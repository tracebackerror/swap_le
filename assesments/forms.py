from django import forms
from django.contrib.auth.models import User
from .models import Assesment, Question, Answer, Result

from students.models import Student
from django.forms.models import modelformset_factory, inlineformset_factory
from django.db.models import Count

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field, Fieldset, Reset
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from django.template.defaultfilters import default


class QuestionForm(forms.ModelForm):
    question_image = forms.ImageField(required=False)
    question_text = forms.CharField(label="Question ", widget=forms.Textarea(attrs={'rows':14, 'cols':50}))
    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        
        
    
    class Meta:
        model   = Question
        fields  = ('__all__')
        exclude = ['deleted_by','deleted_at', 'created_by', 'updated_by', 'assesment_linked']
    
    

    
    


class ReviewSqaAnswerForm(forms.ModelForm):
    written_answer = forms.CharField(label="Written Brief Answer: ", widget=forms.Textarea(attrs={'rows':7, 'cols':50}))
    def __init__(self, *args, **kwargs):
        super(ReviewSqaAnswerForm, self).__init__(*args, **kwargs)
        #self.fields['question_text']=forms.ModelChoiceField(queryset=Question.objects.filter(question_text="sdf"))
            
        
        
    class Meta:
        model   = Answer
        fields  = ['for_question','written_answer', 'alloted_marks']
        exclude = ['deleted_by','deleted_at', 'created_by', 'updated_by','opted_choice','for_result']
        widgets = {
          'written_answer': forms.Textarea(attrs={'rows':14, 'cols':50}),
        }


ReviewSqaFormSetBase = modelformset_factory(Answer,extra=0,form=ReviewSqaAnswerForm)

class ReviewSqaFormSet(ReviewSqaFormSetBase):
  
  def add_fields(self, form, index):
    super(ReviewSqaFormSet, self).add_fields(form, index)
    #form.fields['is_checked'] = forms.BooleanField(required=False)
    #form.fields['somefield'].widget.attrs['class'] = 'somefieldclass'

class ReviewSqaFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(ReviewSqaFormSetHelper, self).__init__(*args, **kwargs)
        
        self.form_method = 'post'
        self.form_action = '.'
        self.layout = Layout(
                                    Field('for_question',style="height: 34px;", title="Question text of the asked answer?", css_class="select", css_id="",readonly=True),
                                    Field('written_answer',style="", title="Question text of the asked answer?", css_class="select", css_id="", readonly=True),
                                    Field('alloted_marks',style="height: 34px;", title="Question text of the asked answer?", css_class="select", css_id=""),
                                    
                                    #FormActions(Submit('submit', 'Update Marks'))
            
                                )
        self.add_input(Submit("submit", "Update Marks"))
        self.render_required_fields = True
        
class CustomOptionsForAssesment(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
         return obj.get_student_name_for_staff()
        
        
class AssessmentForm(forms.ModelForm):
    DURATION_HOURS_CHOICES = [
        (i,i) for i in range(0,24)
        ]
    
    DURATION_MINUTES_CHOICES = [
        (i,i) for i in range(0,60)
        ]
    
    duration_hours = forms.ChoiceField(choices=DURATION_HOURS_CHOICES, required=True)
    duration_minutes = forms.ChoiceField(choices=DURATION_MINUTES_CHOICES, required=True)
    
    expired_on = forms.DateTimeField(
                                input_formats=['%d/%m/%Y %H:%M'],
                                widget=forms.DateTimeInput(attrs={
                                                                'class': 'form-control datetimepicker-input',
                                                                'data-target': '#expired_on'
                                                            }),
                                                          
                               )
                               
    exam_start_date_time = forms.DateTimeField(
                                input_formats=['%d/%m/%Y %H:%M'],
                                widget=forms.DateTimeInput(attrs={
                                                                'class': 'form-control datetimepicker-input',
                                                                'data-target': '#datetimepicker1'
                                                            }),
                                                          
                               )
    
    
    subscriber_users = CustomOptionsForAssesment(queryset = Student.objects.filter(id=1),
                                                      widget=forms.CheckboxSelectMultiple())
    
    
    
    class Meta:
        model = Assesment
        
        fields = ('__all__')
        exclude= ['deleted_by','deleted_at', 'created_by', 'updated_by', 'exam_start_type','total_exam_duration', 'is_exam_active']
        labels = {
        "header": "Short Heading",
        "privilege": "Visibility",
        }
        widgets = {
            'header': forms.TextInput(
                                       attrs={'class':'form-control'}
                                    ),
            'brief': forms.Textarea(
                                       attrs={'class':'form-control'}
                                    ),
            
            'passing_marks'         : forms.NumberInput(attrs={'class':'form-control',}),
            'privilege'             : forms.Select(attrs={'class':'custom-select custom-select-md mb-3', 'data-toggle':"tooltip", 'data-placement':"right", 'title':"<h5>Public: Assesment Visibile to Students \n Private and Protected: Only To Staff</h3>"}),
            

        }
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(AssessmentForm, self).__init__(*args, **kwargs)
        
        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        #self.helper = FormHelper(self)
        self.fields["subscriber_users"].queryset = Student.active.filter(staffuser__institute = self.request.user.staff.institute)   
         
class AssessmentCreationForm(forms.ModelForm):
    DURATION_HOURS_CHOICES = [
        (i,i) for i in range(0,24)
        ]
    
    DURATION_MINUTES_CHOICES = [
        (i,i) for i in range(0,60)
        ]
    
    duration_hours = forms.ChoiceField(choices=DURATION_HOURS_CHOICES, required=True)
    duration_minutes = forms.ChoiceField(choices=DURATION_MINUTES_CHOICES, required=True)
    
    expired_on = forms.DateTimeField(
                                input_formats=['%d/%m/%Y %H:%M'],
                                widget=forms.DateTimeInput(attrs={
                                                                'class': 'form-control datetimepicker-input',
                                                                'data-target': '#expired_on'
                                                            }),
                                                          
                               )
                               
    exam_start_date_time = forms.DateTimeField(
                                input_formats=['%d/%m/%Y %H:%M'],
                                widget=forms.DateTimeInput(attrs={
                                                                'class': 'form-control datetimepicker-input',
                                                                'data-target': '#datetimepicker1'
                                                            }),
                                                          
                               )

    subscriber_users = CustomOptionsForAssesment(queryset = Student.objects.filter(id=1),
                                                      widget=forms.CheckboxSelectMultiple())
    
    class Meta:
        model = Assesment
        fields = ('__all__')
        exclude= ['deleted_by','deleted_at', 'created_by', 'updated_by', 'exam_start_type','total_exam_duration', 'is_exam_active']
        
        labels = {
        "header": "Short Heading",
        "privilege": "Visibility",
        }
        widgets = {
            'header': forms.TextInput(
                                       attrs={'class':'form-control'}
                                    ),
            'brief': forms.Textarea(
                                       attrs={'class':'form-control'}
                                    ),
            
            'passing_marks'         : forms.NumberInput(attrs={'class':'form-control',}),
            'privilege'             : forms.Select(attrs={'class':'custom-select custom-select-md mb-3', 'data-toggle':"tooltip", 'data-placement':"right", 'title':"Public: Assessment Visible to Students. \n\n Private and Protected: Assessment Visible Only To Staff"}),
            
                   
            
        }    
       
    
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(AssessmentCreationForm, self).__init__(*args, **kwargs)
        self.fields["subscriber_users"].queryset = Student.active.filter(staffuser__institute = self.request.user.staff.institute)    
    
    
    
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

# Grouping Field M2M
from functools import partial
from itertools import groupby
from operator import attrgetter
from django.forms.models import ModelChoiceIterator, ModelChoiceField


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
        
        self.fields['written_answer'].required = False    
        
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
        
class GroupedModelChoiceIterator(ModelChoiceIterator):
    def __init__(self, field, groupby):
        self.groupby = groupby
        super().__init__(field)

    def __iter__(self):
        if self.field.empty_label is not None:
            yield ("", self.field.empty_label)
        queryset = self.queryset
        # Can't use iterator() when queryset uses prefetch_related()
        if not queryset._prefetch_related_lookups:
            queryset = queryset.iterator()
        for group, objs in groupby(queryset, self.groupby):
            yield (group, [self.choice(obj) for obj in objs])

    
       
class GroupedModelChoiceField(ModelChoiceField):
    def __init__(self, *args, choices_groupby, **kwargs):
        if isinstance(choices_groupby, str):
            choices_groupby = attrgetter(choices_groupby)
        elif not callable(choices_groupby):
            raise TypeError('choices_groupby must either be a str or a callable accepting a single argument')
        self.iterator = partial(GroupedModelChoiceIterator, groupby=choices_groupby)
        super().__init__(*args, **kwargs)
    
    def to_python(self, value):
        #import pdb; pdb.set_trace()
        value = [ student_data for student_data in value if student_data]
        try:
            value = super(GroupedModelChoiceField, self).to_python(value)
            import pdb; pdb.set_trace()
        except Exception as e:
            
            #key = self.to_field_name or 'pk'
            
            #value = self.queryset.get(**{'pk': value})
            value = self.queryset.filter(pk__in = value)
            if not value.exists():
               raise ValidationError(self.error_messages['invalid_choice'], code='invalid_choice')
            '''else:
               value= value.first()'''
        #import pdb; pdb.set_trace()       
        return value
        
    def prepare_value(self, value):
        #import pdb; pdb.set_trace()
        
        if  type(value) == Student:
            return value.pk
        elif value and len(value) > 0:
            v = [selected.pk for selected in value]
            '''
            if self.to_field_name:
                return value.serializable_value(self.to_field_name)
            else:
                return value.pk'''
                
            return v
        return super().prepare_value(value)
    def has_changed(self, initial, data):
        #import pdb; pdb.set_trace()
        if self.disabled:
            return False
        if initial is None:
            initial = []
        if data is None:
            data = []
        if len(initial) != len(data):
            return True
        initial_set = {str(value) for value in self.prepare_value(initial)}
        data_set = {str(value) for value in data}
        return data_set != initial_set 

        
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
    
    
    subscriber_users = GroupedModelChoiceField(
                                queryset=Student.objects.none(), 
                                choices_groupby='staffuser',
                                widget= forms.SelectMultiple
                                )   
    '''
    def clean_subscriber_users(self):
        student = self.cleaned_data['subscriber_users']
        
        import pdb; pdb.set_trace()
        #forms.ValidationError("By Pass Validation")
        return student
    '''
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
        initial = {
            'privilege': 'public'
        }
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(AssessmentForm, self).__init__(*args, **kwargs)
        
        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        #self.helper = FormHelper(self)
        #self.fields["subscriber_users"].queryset = Student.active.filter(staffuser__institute = self.request.user.staff.institute)   
        self.fields["subscriber_users"].queryset = Student.active.filter(staffuser__institute = self.request.user.staff.institute).exclude(staffuser=None) 
         
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

    subscriber_users = GroupedModelChoiceField(
                                queryset=Student.objects.none(), 
                                choices_groupby='staffuser',
                                widget= forms.SelectMultiple
                                )
    
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
        #self.fields["subscriber_users"].queryset = Student.active.filter(staffuser__institute = self.request.user.staff.institute)    
        self.fields["subscriber_users"].queryset = Student.active.filter(staffuser__institute = self.request.user.staff.institute).exclude(staffuser=None)   
    
    
    
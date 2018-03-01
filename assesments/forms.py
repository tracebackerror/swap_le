from django import forms
from django.contrib.auth.models import User
from .models import Assesment, Question, Answer

from students.models import Student
from django.forms.models import modelformset_factory

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field, Fieldset, Reset
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions


class QuestionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        
        super(QuestionForm, self).__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = '.'
        self.helper.form_id = 'action_question_add'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8'
        self.helper.form_show_errors = True
        self.helper.form_error_title = "error of form"
        self.helper.formset_error_title ="E formset"
        self.helper.layout = Layout(
                                Fieldset(
                                    'Please Use the below form for adding a Question to Assesment',
                                   'question_text',
                                   'max_marks',
                                   
                                   Field('question_type',style="height: 34px;", title="What kind of question you want to create ?", css_class="select", css_id="which_question"),
                                   
                                   Field('brief_answer',style="", title="Please Enter Correct Answer For Reference", css_class="", css_id="reference_answer"),
                                   Div(
                                   Field('option_one',style="", title="Please Enter Option For Answer", css_class="", css_id="option_one"),
                                   Field('option_two',style="", title="Please Enter Option For Answer", css_class="", css_id="option_two"),
                                   Field('option_three',style="", title="Please Enter Option For Answer", css_class="", css_id="option_three"),
                                   Field('option_four',style="", title="Please Enter Option For Answer", css_class="", css_id="option_four"),
                                   Field('option_five',style="", title="Please Enter Option For Answer", css_class="", css_id="option_five"),
                                   
                                   Field('correct_options', type='hidden', style="", title="", css_class=""),
                                   css_id = 'option-fields'
                                   ),
                                   
                                ),
                                 HTML("""
                                        <p>Please click on submit, <strong>for creating the question</strong></p>
                                """),
                                    FormActions(Submit('submit', 'Submit'), Reset('name', 'Reset') )
                            )
        #self.helper.add_input()
        
    
    class Meta:
        model   = Question
        fields  = ('__all__')
        exclude = ['deleted_by','deleted_at', 'created_by', 'updated_by', 'assesment_linked']
    
    

    
    


class ReviewSqaAnswerForm(forms.ModelForm):
    written_answer = forms.CharField(label="Written Brief Answer: ", widget=forms.Textarea(attrs={'rows':14, 'cols':50}))
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
                                    Field('written_answer',style="height: 34px;", title="Question text of the asked answer?", css_class="select", css_id="", readonly=True),
                                    Field('alloted_marks',style="height: 34px;", title="Question text of the asked answer?", css_class="select", css_id=""),
                                    
                                    #FormActions(Submit('submit', 'Update Marks'))
            
                                )
        self.add_input(Submit("submit", "Update Marks"))
        self.render_required_fields = True
        
        
class AssessmentForm(forms.ModelForm):
    start_time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'), help_text="HH:MM")
    end_time   = forms.TimeField(widget=forms.TimeInput(format='%H:%M'), help_text="HH:MM")
    exam_date  = forms.DateField(input_formats='%Y-%m-%d',help_text="2006-10-25")
    
    class Meta:
        model = Assesment
        fields = ('__all__')
        exclude= ['deleted_by','deleted_at', 'created_by', 'updated_by']
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(AssessmentForm, self).__init__(*args, **kwargs)
        
        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.fields["subscriber_users"].queryset = Student.active.filter(staffuser__institute = self.request.user.staff.institute)   
        

class AssessmentCreationForm(forms.ModelForm):
    start_time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'), help_text="HH:MM")
    end_time   = forms.TimeField(widget=forms.TimeInput(format='%H:%M'), help_text="HH:MM")
    #exam_date  = forms.DateField(widget=forms.DateInput(attrs={'id': 'myCustomId',}), input_formats='%Y-%m-%d',help_text="YYYY-MM-DD")
    
    
    class Meta:
        model = Assesment
        fields = ('__all__')
        exclude= ['deleted_by','deleted_at', 'created_by', 'updated_by']
        widgets = {
            'exam_date': forms.DateInput(format=('%d-%m-%Y'), 
                                             attrs={'class':'myDateClass', 
                                            'placeholder':'Select a date'},
                                        )
        }
        
       
    
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(AssessmentCreationForm, self).__init__(*args, **kwargs)
        self.fields["subscriber_users"].queryset = Student.active.filter(staffuser__institute = self.request.user.staff.institute)    
    
    
    
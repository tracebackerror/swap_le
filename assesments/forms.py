from django import forms
from django.contrib.auth.models import User
from .models import Assesment, Question

from students.models import Student

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
        self.helper.label_class = 'col-lg-2'
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
    
    
    
        
class AssessmentForm(forms.ModelForm):
    """
    header = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Header'}
    ), required=True)

    slug = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Slug'}
    ), required=True)

    brief = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Brief'}
    ), required=True)
    """
    
    start_time=forms.DateTimeField(widget=forms.DateTimeInput)
    
    
    
    
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
    
    class Meta:
        model = Assesment
        fields = ('__all__')
        exclude= ['deleted_by','deleted_at', 'created_by', 'updated_by']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'class': 'datetime-input'})
        }
    
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(AssessmentCreationForm, self).__init__(*args, **kwargs)
        self.fields["subscriber_users"].queryset = Student.active.filter(staffuser__institute = self.request.user.staff.institute)    
    
    
    
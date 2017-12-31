from django import forms
from django.contrib.auth.models import User
from .models import Assesment, Question

from students.models import Student

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions


class QuestionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        
        super(QuestionForm, self).__init__(*args, **kwargs)
       
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = '.'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.add_input(Submit('submit', 'Submit'))
   
    class Meta:
        model = Question
        fields = ('__all__')
        exclude= ['deleted_by','deleted_at', 'created_by', 'updated_by', 'assesment_linked']
    
    
    
        
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
    
    
    
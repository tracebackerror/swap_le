from django import forms
from .models import Student
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from institutions.models import Institutions
from staff.models import Staff


class StudentAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StudentAdminForm, self).__init__(*args, **kwargs)
        self.fields['studentuser'].required = True
        self.fields['staffuser'].required = True
        
    class Meta:
        model = Student
        fields = ('studentuser', 'staffuser', 'deleted')
        

class StudentRegistrationForm(UserCreationForm):
    institution_name = forms.ModelChoiceField(queryset=Institutions.objects.all(),label="Institutions Name",required=True)
    staffuser = forms.ModelChoiceField(queryset=Staff.objects.all(),label="Staff Name",required=True)
    first_name = forms.CharField(widget=forms.TextInput,required=True)
    last_name = forms.CharField(widget=forms.TextInput,required=True)
    email = forms.EmailField(widget=forms.EmailInput,required=True)
    standard = forms.CharField(widget=forms.TextInput,required=True)
    address = forms.CharField(widget=forms.Textarea,required=True)
    student_contact_no = forms.IntegerField(widget=forms.NumberInput,required=True)
    parent_contact_no = forms.IntegerField(widget=forms.NumberInput,required=True)
    gender = forms.ChoiceField(widget=forms.RadioSelect(attrs={'style': 'width: 50px;'}),choices=(('male','Male'),('female','Female')))
    
    def clean_student_contact_no(self):
        data = self.cleaned_data['student_contact_no']
        if len(str(data)) != 10:
            raise forms.ValidationError("Invalid Mobile Number : Enter 10 digit mobile number")
        
    def clean_parent_contact_no(self):
        data = self.cleaned_data['parent_contact_no']
        if len(str(data)) != 10:
            raise forms.ValidationError("Invalid Mobile Number : Enter 10 digit mobile number")
    
    def __init__(self,*args, **kwargs):
        super(StudentRegistrationForm, self).__init__(*args, **kwargs)
        if 'data' in kwargs:
            institution_id = kwargs.get('data')['institution_name']
            instition_obj = Institutions.objects.get(id=institution_id)
            self.fields['staffuser'].queryset = Staff.objects.filter(institute = instition_obj)

        
    class Meta:
        model=User
        fields = ['username','first_name','last_name','email','password1','password2']
        
        


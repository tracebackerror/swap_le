from .models import Institutions
from django import forms
from django.contrib.auth.models import User
from staff.models import Staff,StudentEnquiry
from students.models import Student

from django.forms import widgets
from django.contrib.auth.forms import UserCreationForm


class StaffEditForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ('__all__')
        # exclude= ['institute_status','user']
        
        
class EnrollStudentsForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['allowregistration',]
        # exclude= ['institute_status','user']

class StudentEditForm(forms.ModelForm):
    standard = forms.CharField(widget=forms.TextInput,required=True)
    address = forms.CharField(widget=forms.Textarea,required=True)
    student_contact_no = forms.IntegerField(widget=forms.NumberInput,required=True)
    parent_contact_no = forms.IntegerField(widget=forms.NumberInput,required=True)
    
    class Meta:
        model=Student
        fields=['standard','address','student_contact_no','parent_contact_no']     

class StudentUserEditForm(forms.ModelForm):    
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
        
        
class StudentAddForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput,required=True)
    last_name = forms.CharField(widget=forms.TextInput,required=True)
    email = forms.EmailField(widget=forms.EmailInput,required=True)
    standard = forms.CharField(widget=forms.TextInput,required=True)
    address = forms.CharField(widget=forms.Textarea,required=True)
    student_contact_no = forms.IntegerField(widget=forms.NumberInput,required=True)
    parent_contact_no = forms.IntegerField(widget=forms.NumberInput,required=True)
    
    class Meta:
        model=User
        fields = ['username','first_name','last_name','email','password1','password2']

   
class CreateStudentEnquiryForm(forms.ModelForm):
    full_name=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'First Name    Middle Name    Last Name'}),label='Student Full Name')
    parent_name=forms.CharField(widget=forms.TextInput(),label='Parent Name')
    scl_clg_name=forms.CharField(widget=forms.TextInput(),label="School Name / College Name")
    std=forms.CharField(widget=forms.TextInput(),label='Standard')
    academic_y=forms.CharField(widget=forms.TextInput(),label='Academic Year')
    contact=forms.IntegerField(widget=forms.NumberInput(),label='Contact Number')

    class Meta:
        model=StudentEnquiry
        fields=['full_name','parent_name','scl_clg_name','std','academic_y','contact']
    
        
        
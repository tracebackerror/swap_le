from .models import Institutions
from django import forms
from django.contrib.auth.models import User
from staff.models import Staff,StudentEnquiry
from students.models import Student
from django.forms import widgets
from django.contrib.auth.forms import UserCreationForm
from utility.swaple_constants import COURSE_CHOICES

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
    gender = forms.ChoiceField(widget=forms.RadioSelect(attrs={'style': 'width: 50px;'}),choices=(('male','Male'),('female','Female')))
    
    class Meta:
        model=Student
        fields=['standard','address','student_contact_no','parent_contact_no','gender']     

class StudentUserEditForm(forms.ModelForm):    
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
        
        
class StudentAddForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput,required=True)
    last_name = forms.CharField(widget=forms.TextInput,required=True)
    email = forms.EmailField(widget=forms.EmailInput,required=True)
    standard = forms.CharField(widget=forms.Select(choices=COURSE_CHOICES),required=True)
    address = forms.CharField(widget=forms.Textarea,required=True)
    student_contact_no = forms.CharField(required=True, min_length=10, max_length=10)
    parent_contact_no = forms.CharField(required=False, min_length=10, max_length=10)
    gender = forms.ChoiceField(widget=forms.RadioSelect(attrs={'style': 'width: 50px;'}),choices=(('male','Male'),('female','Female')))
    
    def __init__(self,*args, **kwargs):
        super(StudentAddForm, self).__init__(*args, **kwargs)
        
        for fieldname in [ 'password1', 'password2']:
            self.fields[fieldname].help_text = None
            
    def clean_student_contact_no(self):
        data = self.cleaned_data['student_contact_no']
        if len(str(data)) != 10:
            raise forms.ValidationError("Invalid Mobile Number : Enter 10 digit mobile number")
        
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
    
        
        
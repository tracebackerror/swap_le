from .models import Institutions
from django import forms
from django.contrib.auth.models import User
from staff.models import Staff
from students.models import Student
from tkinter import Widget
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
    #studentuser = forms.CharField()
    #staffuser = forms.CharField() 
    class Meta:
        model = Student
        fields = ['studentuser','staffuser']
        

class StudentUserEditForm(forms.ModelForm):
     class Meta:
        model = User
        fields = ['first_name','last_name','email']
        
        
class StudentAddForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput,required=True)
    last_name = forms.CharField(widget=forms.TextInput,required=True)
    email = forms.EmailField(widget=forms.EmailInput,required=True)
    
    class Meta:
        model=User
        fields = ['username','first_name','last_name','email','password1','password2']
        
        
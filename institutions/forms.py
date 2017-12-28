from .models import Institutions
from django import forms
from django.contrib.auth.models import User
from staff.models import Staff
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin import widgets


class StaffProfileForm(forms.ModelForm):

    class Meta:
        model = Staff
        fields = ('__all__')

        #fields = ('username', 'birth_date', 'password1', 'password2', )

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        exclude = []
        
class InstitutionsEditForm(forms.ModelForm):
    class Meta:
        model = Institutions
        fields = ('__all__')
        exclude= ['institute_status','user']

class InstitutionLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput) 
    
    
class StaffCreateForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput,required=True)
    last_name = forms.CharField(widget=forms.TextInput,required=True)
    email = forms.EmailField(widget=forms.EmailInput,required=True)
    
    
    class Meta:
        model=User
        fields = ['username','first_name','last_name','email','password1','password2']
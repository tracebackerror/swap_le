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
        
        
class InstitutionRegistrationForm(UserCreationForm):
    institute_name = forms.CharField(widget = forms.TextInput,required = True,label = "Institution Name")
    email =  forms.EmailField(widget = forms.EmailInput,label = "Email",required = False)
    username = forms.CharField(widget = forms.TextInput,required = True,label = "Institution Username")
    institute_contact_mobile = forms.CharField(widget = forms.NumberInput,required = True,label = "Contact Number")
    institute_contact_landline = forms.CharField(widget = forms.NumberInput,required = False, label = "Landline Number")
    institute_address = forms.CharField(widget = forms.TextInput,required = True,label = "Address") 
    institute_city = forms.CharField(widget = forms.TextInput,required = True,label = "City")
    institute_state = forms.CharField(widget = forms.TextInput,required = True,label = "State")
    institute_country = forms.CharField(widget = forms.TextInput,required = True,label = "Country")
    
    def __init__(self,*args, **kwargs):
        super(InstitutionRegistrationForm, self).__init__(*args, **kwargs)
        
        for fieldname in [ 'password1', 'password2']:
            self.fields[fieldname].help_text = None
            
            
    def clean_institute_contact_mobile(self):
        data = self.cleaned_data['institute_contact_mobile']
        if len(str(data)) != 10:
            raise forms.ValidationError("Invalid Contact Number : Enter 10 digit Contact Number")
    
    
    class Meta:
        model=User
        fields = ['username','first_name','last_name','email','password1','password2']
        
    
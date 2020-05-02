from .models import Institutions
from django import forms
from django.contrib.auth.models import User
from staff.models import Staff
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin import widgets
from localflavor.in_.forms import INStateSelect
from django_countries.widgets import CountrySelectWidget
from django_countries.fields import CountryField

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit

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
    institute_state = forms.CharField(widget = INStateSelect,required = True,label = "State")
    institute_name = forms.CharField(widget = forms.TextInput,required = True,label = "Institution Name")
    email =  forms.EmailField(widget = forms.EmailInput,label = "Email",required = False)
    username = forms.CharField(widget = forms.TextInput,required = True,label = "Institution Username", help_text= " " )
    institute_contact_mobile = forms.CharField(widget = forms.TextInput, min_length=10, max_length=10,required = True,label = "Contact Number")
    institute_contact_landline = forms.CharField(widget = forms.TextInput, min_length=10, max_length=10, required = False, label = "Landline Number")
    institute_address = forms.CharField(widget = forms.TextInput,required = True,label = "Address") 
    institute_city = forms.CharField(widget = forms.TextInput,required = True,label = "City")
    institute_state = forms.CharField(widget = INStateSelect,required = True,label = "State")
    #institute_country = forms.CharField(widget = forms.TextInput,required = True,label = "Country")
    institute_country = CountryField().formfield()
    
    def __init__(self,*args, **kwargs):
        super(InstitutionsEditForm, self).__init__(*args, **kwargs)
        
        for fieldname in [ 'username', ]:
            self.fields[fieldname].help_text = None
            
        
    class Meta:
        model = Institutions
        fields = ('__all__')
        exclude= ['institute_status','user']

class InstitutionLoginForm(forms.Form):
    username = forms.CharField()
    
    password = forms.CharField(widget=forms.PasswordInput) 
    
    def __init__(self, *args, **kwargs):
        
        super(InstitutionLoginForm, self).__init__(*args, **kwargs)
    
    
class StaffCreateForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput,required=True)
    last_name = forms.CharField(widget=forms.TextInput,required=True)
    email = forms.EmailField(widget=forms.EmailInput,required=True)
    
    def __init__(self,*args, **kwargs):
        super(StaffCreateForm, self).__init__(*args, **kwargs)
        
        for fieldname in [ 'password1', 'password2', 'username']:
                self.fields[fieldname].help_text = None
    class Meta:
        model=User
        fields = ['username','first_name','last_name','email','password1','password2']
        
        
class InstitutionRegistrationForm(UserCreationForm):
    institute_name = forms.CharField(widget = forms.TextInput,required = True,label = "Institution Name")
    email =  forms.EmailField(widget = forms.EmailInput,label = "Email",required = False)
    username = forms.CharField(widget = forms.TextInput,required = True,label = "Institution Username")
    institute_contact_mobile = forms.CharField(widget = forms.TextInput,min_length=10, max_length=10,required = True,label = "Contact Number")
    institute_contact_landline = forms.CharField(widget = forms.TextInput, min_length=10, max_length=10, required = False, label = "Landline Number")
    institute_address = forms.CharField(widget = forms.TextInput,required = True,label = "Address") 
    institute_city = forms.CharField(widget = forms.TextInput,required = True,label = "City")
    institute_state = forms.CharField(widget = INStateSelect,required = True,label = "State")
    #institute_country = forms.CharField(widget = forms.TextInput,required = True,label = "Country")
    institute_country = CountryField().formfield()
    
    def __init__(self,*args, **kwargs):
        super(InstitutionRegistrationForm, self).__init__(*args, **kwargs)
        
        for fieldname in [ 'password1', 'password2']:
            self.fields[fieldname].help_text = None
            
        self.fields['institute_contact_landline'].required = False
        
    def clean_institute_contact_mobile(self):
        data = self.cleaned_data['institute_contact_mobile']
        if len(str(data)) != 10:
            raise forms.ValidationError("Invalid Contact Number : Enter 10 digit Contact Number")
    
    
    class Meta:
        model=User
        fields = ['username','first_name','last_name','email','password1','password2']
        
        #widgets = {'institute_country': CountrySelectWidget()}
    
    
from django import forms
from django.contrib.auth.models import User
from .models import Assesment

from students.models import Student



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
        self.fields["subscriber_users"].queryset = Student.active.filter(staffuser = self.request.user.staff)   
        

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
        self.fields["subscriber_users"].queryset = Student.active.filter(staffuser = self.request.user.staff)    
    
    
    
from django import forms
from django.contrib.auth.models import User
from .models import Assesment



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
    
    class Meta:
        model = Assesment
        fields = ['header', 'slug', 'brief']
from django import forms
from .models import Section

class AddQuestionSectionForm(forms.ModelForm):
    name = forms.CharField(widget = forms.TextInput(),required = True, label="Section Name")
    
    class Meta():
        model = Section
        fields = ['name']
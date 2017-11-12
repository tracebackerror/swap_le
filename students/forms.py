from django import forms
from .models import Student



class StudentAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StudentAdminForm, self).__init__(*args, **kwargs)
        self.fields['studentuser'].required = True
        self.fields['staffuser'].required = True
        
    class Meta:
        model = Student
        fields = ('studentuser', 'staffuser', 'deleted')
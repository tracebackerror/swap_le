from .models import Institutions
from django import forms
from django.contrib.auth.models import User
from staff.models import Staff


class StaffEditForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ('__all__')
        # exclude= ['institute_status','user']

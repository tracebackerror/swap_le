from django import forms
from licenses.models import License
from django.utils.translation import gettext_lazy as _

from django.forms import widgets


class LicenseViewForm(forms.ModelForm):
    li_current_status = forms.TextInput(attrs={'disabled': True})


    class Meta:
        model = License
        fields = ('li_key', 'li_expiration_date', 'li_max_staff', 'li_max_students', 'li_max_assesments',
                  'li_current_staff', 'li_max_assesments', 'li_current_staff', 'li_current_students',
                  'li_current_assesments', 'li_current_status'
                  )

        labels = {
            'li_key': _('Institution License Number'),
            'li_expiration_date' : _('Deactivated After'),

            'li_max_staff': _('Maximum Allowed Staff'),
            'li_max_students': _('Maximum Allowed Students'),
            'li_max_assesments': _('Maximum Allowed Assessments'),
            'li_current_staff': _('Total Active Staff'),
            'li_current_students': _('Total Active Students'),
            'li_current_assesments': _('Total Exhausted Assessment'),
            'li_current_status': _('Institution State'),
        }

        widgets = {
            'li_key':  forms.TextInput(attrs={'disabled': True}),
            'li_expiration_date': forms.TextInput(attrs={'disabled': True}),

            'li_max_staff': forms.TextInput(attrs={'disabled': True}),
            'li_max_students': forms.TextInput(attrs={'disabled': True}),
            'li_max_assesments': forms.TextInput(attrs={'disabled': True}),
            'li_current_staff': forms.TextInput(attrs={'disabled': True}),
            'li_current_students': forms.TextInput(attrs={'disabled': True}),
            'li_current_assesments': forms.TextInput(attrs={'disabled': True}),
            'li_current_status': forms.Select(attrs={'disabled': True})
        }


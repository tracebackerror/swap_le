from django import forms
from datetime import datetime
from .models import FeesInstallment

class InstallmentFeesForm(forms.ModelForm):
    MONTH_NAMES_CHOICES = (
        ('JAN','January'),
        ('FEB','February'),
        ('MAR','March'),
        ('APR','April'),
        ('MAY','May'),
        ('JUN','June'),
        ('JUL','July'),
        ('AUG','August'),
        ('SEP','September'),
        ('OCT','October'),
        ('NOV','November'),
        ('DEC','December'),
        )
    curr_yr = datetime.now().year
    YEAR_CHOICES = [ (curr_yr-3,curr_yr-3),(curr_yr-2,curr_yr-2),(curr_yr-1,curr_yr-1) ]
    for x in range(curr_yr,curr_yr + 11):
        YEAR_CHOICES.append((curr_yr,curr_yr))
        curr_yr+=1
    
    amount = forms.FloatField(widget = forms.NumberInput ,label="Amount",required=True)
    day = forms.ChoiceField(choices = [(x, x) for x in range(1, 32)] ,label="Day")
    month = forms.ChoiceField(choices = MONTH_NAMES_CHOICES ,label="Month")
    year = forms.ChoiceField(choices = YEAR_CHOICES ,label="Year")
    paid = forms.BooleanField(widget = forms.CheckboxInput ,label="Paid",required=False)
    
    class Meta():
        model = FeesInstallment
        fields = ['amount','day','month','year','paid']
import django_filters
from .models import FeesInstallment
from datetime import datetime

class FeesInstallmentFilter(django_filters.FilterSet):
    curr_yr = datetime.now().year
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
    YEAR_CHOICES = [ (curr_yr-3,curr_yr-3),(curr_yr-2,curr_yr-2),(curr_yr-1,curr_yr-1) ]
    for x in range(curr_yr,curr_yr + 11):
        YEAR_CHOICES.append((curr_yr,curr_yr))
        curr_yr+=1
    
    amount = django_filters.NumberFilter(lookup_expr = "icontains")
    day = django_filters.ChoiceFilter(choices = [(x, x) for x in range(1, 32)])
    month = django_filters.ChoiceFilter(choices = MONTH_NAMES_CHOICES)
    year = django_filters.ChoiceFilter(choices = YEAR_CHOICES)
    paid = django_filters.BooleanFilter()
    class Meta:
        model = FeesInstallment
        fields = ['amount','day','month','year','paid']

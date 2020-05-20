import django_filters
from fees.models import FeesInstallment
from datetime import datetime
from students.models import Student
from .models import Institutions
from staff.models import Staff
class ViewFeesInstallmentFilter(django_filters.FilterSet):
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
    
    student_id = django_filters.ModelChoiceFilter()
    amount = django_filters.NumberFilter(lookup_expr = "icontains")
    day = django_filters.ChoiceFilter(choices = [(x, x) for x in range(1, 32)])
    month = django_filters.ChoiceFilter(choices = MONTH_NAMES_CHOICES)
    year = django_filters.ChoiceFilter(choices = YEAR_CHOICES)
    paid = django_filters.BooleanFilter()
    
    class Meta:
        model = FeesInstallment
        fields = ['student_id','amount','day','month','year','paid']               
                
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        institute = Institutions.objects.get(user__username =  self.request.user)
        self.get_filters().get('student_id').queryset = Student.objects.filter(staffuser__institute = institute)
        super(ViewFeesInstallmentFilter, self).__init__(*args, **kwargs)

        
class StaffFilter(django_filters.FilterSet):
    #first_name = django_filters.CharFilter(field_name='relationship__name', lookup_expr='contains')
    class Meta:
        model = Staff
        fields = {
            
            'staffuser__first_name' : ['icontains'],
            'staffuser__last_name' : ['icontains'],
            'staffuser__email' : ['icontains'],
            'staffuser__username' : ['icontains'],
            
            }    

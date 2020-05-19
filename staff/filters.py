from .models import StudentEnquiry
import django_filters

from students.models import *

class StudentEnquiryFilter(django_filters.FilterSet):
    class Meta:
        model = StudentEnquiry
        fields = {
                       
            'full_name': ['icontains']
        }
class StudentFilter(django_filters.FilterSet):
    #first_name = django_filters.CharFilter(field_name='relationship__name', lookup_expr='contains')
    class Meta:
        model = Student
        fields = {
            
            'studentuser__first_name' : ['icontains'],
            'studentuser__last_name' : ['icontains'],
            'studentuser__email' : ['icontains'],
            'student_contact_no' : ['icontains'],
            'standard' : ['icontains'],
            
            }
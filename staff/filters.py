from .models import StudentEnquiry
import django_filters


class StudentEnquiryFilter(django_filters.FilterSet):
    class Meta:
        model = StudentEnquiry
        fields = {
                       
            'full_name': ['icontains']
        }

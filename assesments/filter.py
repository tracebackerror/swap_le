from .models import Assesment

from django_filters import FilterSet, CharFilter

class AssesmentFilter(FilterSet):
    ''' This class provides the capability of filtering the data using django_filter for Assesment Model '''
    class Meta:
        model = Assesment
        
        fields = {
            'header': ['icontains'],
            'brief': ['icontains'],
        }

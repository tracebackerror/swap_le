import django_filters
from library.models import LibraryAsset
from django_filters import FilterSet, CharFilter

class ViewLibraryAssetFilter(django_filters.FilterSet):
    class Meta:
        model = LibraryAsset
        fields = {
            
            'asset_unique_code' : ['icontains'],
            
            'name' : ['icontains']
            
            }
            

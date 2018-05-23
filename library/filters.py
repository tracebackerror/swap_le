import django_filters
from .models import LibraryAsset


class LibraryAssetFilter(django_filters.FilterSet):
    class Meta:
        model = LibraryAsset
        fields = {
            
            'asset_unique_code' : ['icontains'],
            
            'name' : ['icontains']
            
            }
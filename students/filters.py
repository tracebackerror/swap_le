import django_filters
from library.models import LibraryAsset


class ViewLibraryAssetFilter(django_filters.FilterSet):
    class Meta:
        model = LibraryAsset
        fields = {
            
            'asset_unique_code' : ['icontains'],
            
            'name' : ['icontains']
            
            }
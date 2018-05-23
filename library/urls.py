from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^asset/create/',CreateLibraryAsset.as_view(),name="create_library_asset"),
    url(r'^asset/manage/',ManageLibraryAsset.as_view(),name="manage_library_asset"),
    url(r'^asset/(?P<pk>\d+)/delete/$',DeleteLibraryAsset.as_view(),name="delete_library_asset"),
    url(r'^asset/(?P<pk>\d+)/edit/$',EditLibraryAsset.as_view(),name="edit_library_asset"),
    
    url(r'^asset/(?P<pk>\d+)/history/$',ManageLibraryAssetHistory.as_view(),name="manage_library_asset_history"),
    url(r'^asset/(?P<pk>\d+)/history/add/$',AddLibraryAssetHistory.as_view(),name="add_library_asset_history"),
    
    url(r'^asset/(?P<pk>\d+)/history/(?P<id>\d+)/check-in/$',CheckIn,name="check_in"),
    
]

from django.urls import path
from .views import *

app_name = 'library'

urlpatterns = [
    path('asset/create/', CreateLibraryAsset.as_view(), name="create_library_asset"),
    path('asset/manage/', ManageLibraryAsset.as_view(), name="manage_library_asset"),
    path('asset/<int:pk>/delete/', DeleteLibraryAsset.as_view(), name="delete_library_asset"),
    path('asset/<int:pk>/edit/', EditLibraryAsset.as_view(), name="edit_library_asset"),
    
    path('asset/<int:pk>/history/', ManageLibraryAssetHistory.as_view(), name="manage_library_asset_history"),
    path('asset/<int:pk>/history/add/', AddLibraryAssetHistory.as_view(), name="add_library_asset_history"),
    
    path('asset/<int:pk>/history/<int:id>/check-in/', CheckIn, name="check_in"),
]

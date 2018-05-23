from django.contrib import admin
from .models import LibraryAsset,AssetHistory
# Register your models here.

admin.site.register(LibraryAsset)
admin.site.register(AssetHistory)
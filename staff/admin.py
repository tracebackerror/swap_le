from django.contrib import admin

from .models import Staff
# Register your models here.


class StaffAdmin(admin.ModelAdmin):
    list_display = ('staffuser','institute','deleted',)
    #list_filter = ('__all__')
    #search_fields = ('__all__')
    #prepopulated_fields = {'slug': ('title',)}
    #raw_id_fields = ('li_institute',)
    #date_hierarchy = 'li_updated'
    #ordering = ['li_expiration_date', ]
    list_editable = ['institute','deleted']
    list_display_links = ['staffuser']
    readonly_fields = ('user_type',)
    
admin.site.register(Staff, StaffAdmin)
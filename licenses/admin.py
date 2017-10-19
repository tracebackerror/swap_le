from django.contrib import admin

from .models import License
# Register your models here.


class LicenseAdmin(admin.ModelAdmin):
    list_display = ('li_key', 'li_expiration_date','li_created', 'li_updated','li_max_staff','li_max_students', 'li_max_assesments',
    'li_current_staff', 'li_current_students','li_current_assesments', 'li_current_status','li_institute')
    list_filter = ('li_key','li_created', 'li_updated',)
    search_fields = ('li_key',)
    #prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('li_institute',)
    date_hierarchy = 'li_updated'
    ordering = ['li_expiration_date', ]

admin.site.register(License, LicenseAdmin)


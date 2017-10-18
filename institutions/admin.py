from django.contrib import admin
from .models import Institutions
from django.contrib.auth.models import Permission
# Register your models here.
admin.site.register(Permission)
#admin.site.unregister(Institutions)

class InstitutionsAdmin(admin.ModelAdmin):

    readonly_fields = ('deleted', 'user_type'   )



admin.site.register(Institutions,InstitutionsAdmin)

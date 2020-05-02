from django.contrib import admin
from .models import Student
from .forms import StudentAdminForm
from staff.models import Staff
# Register your models here.

class StudentInline(admin.StackedInline):
    model = Student
    #readonly_fields = ['user', 'transaction_type', 'transaction_date']
    #verbose_name = 'Staff'
    #verbose_name_plural = 'Staffs'
    
    
class StaffAdmin(admin.ModelAdmin):
    #fieldsets = [ (None, {'fields': ['title'}) ]
    inlines = [ StudentInline, ]
    
    
    
class StudentAdmin(admin.ModelAdmin):
    form = StudentAdminForm
    list_display = ('studentuser', 'staffuser', 'user_type', 'standard', 'address', 'student_contact_no', 'parent_contact_no', 'gender',)
admin.site.unregister(Staff)
admin.site.register(Staff,StaffAdmin)    
admin.site.register(Student,StudentAdmin)

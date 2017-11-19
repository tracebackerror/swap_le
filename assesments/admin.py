from django.contrib import admin
from .models import Assesment, Question, Result, Answer
# Register your models here.

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1
    #readonly_fields = ['user', 'transaction_type', 'transaction_date']
    #verbose_name = 'Staff'
    #verbose_name_plural = 'Staffs'
    
    
class AssesmentAdmin(admin.ModelAdmin):
    #fieldsets = [ (None, {'fields': ['title'}) ]
    inlines = [ QuestionInline ]
    

#admin.site.unregister(Assesment)
admin.site.register(Assesment, AssesmentAdmin)
admin.site.register(Result)
admin.site.register(Answer)

import django_tables2 as tables
from .models import Staff
import itertools
from django.utils.html import format_html
from students.models import Student
from django_tables2 import A
from django_tables2.export.views import ExportMixin
from django.utils.translation import ugettext_lazy as _

class CustomTemplateColumnEscapeAdmin(tables.TemplateColumn):
    
    def render(self, record, table, value, bound_column, **kwargs):
        
        if record.staffuser.username == record.institute.user.username:
            return format_html('<center><i class="fas fa-user-shield "></i></center>')
        return super(CustomTemplateColumnEscapeAdmin, self).render(record, table, value, bound_column, **kwargs)

class CustomTemplateStudentEscapeAdmin(tables.TemplateColumn):
    
    def render(self, record, table, value, bound_column, **kwargs):
        
        if record.studentuser.has_perm('institutions.is_institute'):
            return format_html('<center><i class="fas fa-user-shield "></i></center>')
        return super(CustomTemplateStudentEscapeAdmin, self).render(record, table, value, bound_column, **kwargs)
        
class StaffTable(ExportMixin, tables.Table):
    export_formats = ['csv', 'xls', ]
    edit_button_html = '<a href=" {% url "institutions:edit_institution_staff" username=record.staffuser  %} "  ><center><span class="fas fa-edit "></span></center></a>'
    delete_button_html = '<a href=" {% url "institutions:delete_institution_staff" username=record.staffuser  %}" ><center><span class="fas fa-trash-alt"></span></center></a>'
    edit_staff = tables.TemplateColumn(edit_button_html, orderable=False) 
    delete_staff = CustomTemplateColumnEscapeAdmin(delete_button_html, orderable=False)
    
    email_student = tables.Column(accessor='staffuser.email',
                          verbose_name='Email')
    first_name = tables.Column(accessor='staffuser.first_name',
                          verbose_name='First Name')
    last_name = tables.Column(accessor='staffuser.last_name',
                          verbose_name='Last Name')
    
    
    def __init__(self, *args, **kwargs):
        super(StaffTable, self).__init__(*args, **kwargs)
        self.counter = itertools.count()

    

    class Meta:
        model = Staff
        # add class="paleblue" to <table> tag
        exclude = ('id', 'deleted', 'user_type', 'institute', 'created', 'updated', 'allowregistration', )
        attrs = {'class': 'paleblue'}
        # fields = ( 'institute',)
        sequence = ( 'staffuser', 'first_name', 'last_name', 'email_student', 'user_type', 'deleted')



class StudentTable(ExportMixin, tables.Table):
    export_formats = ['csv', 'xls', ]
    first_name = tables.Column(accessor='studentuser.first_name',
                               verbose_name='First Name', attrs={"th": {"class": "text-nowrap"}})
    last_name = tables.Column(accessor='studentuser.last_name',
                              verbose_name='Last Name',  attrs={"th": {"class": "text-nowrap"}})
    email = tables.Column(accessor='studentuser.email',
                          verbose_name='Mail Address',  attrs={"th": {"class": "text-nowrap"}})
    
    edit_student = tables.TemplateColumn('<a href=" {% url "staff:student_edit_by_staff" upk=record.pk  %} "><center><span class="fas fa-edit "></span></center></a>', verbose_name="Edit",  attrs={"td": {"class": "text-nowrap"}})
    
    delete_button_html = '<a href=" {% url "staff:delete_institution_staff_student" username=record.studentuser  %} "><center><span class="fas fa-trash-alt"></span></center></a>'
    delete_student = CustomTemplateStudentEscapeAdmin(delete_button_html, orderable=False, verbose_name="Delete")
    #student_fees = tables.TemplateColumn('<a href=" {% url "staff:fees:manage_fees_installment" pk=record.id  %} ">Installment</a>', verbose_name="Fees")
    
    standard = tables.Column(accessor='standard', verbose_name=_('Std.'))
    staffuser = tables.Column(accessor='staffuser', verbose_name=_('Under Professor'))
	
    def __init__(self, *args, **kwargs):
        super(StudentTable, self).__init__(*args, **kwargs)
        self.counter = itertools.count()
    def render_first_name(self,value):
        return value
    
    def render_gender(self,value):
        if value.lower() == "male":
            return format_html('<div class="col-md-12"><center><i class="fa fa-male fa-lg" aria-hidden="true"></i></center></div>', value)
        else:
            return format_html('<div class="col-md-12"><center><i class="fa fa-female fa-lg" aria-hidden="true"></i></center></div>', value)
    
    def render_last_name(self,value):
        return value
    
    def render_email(self,value):
        return value
        
    
    class Meta:
        model = Student
        sequence = ( 'studentuser','first_name','last_name','email', 'staffuser',  )
        # add class="paleblue" to <table> tag 
        attrs = {'class': 'paleblue'}
        # fields = ( 'institute',)
        exclude = ('id', 'deleted', 'last_login', 'created', 'updated', 'user_type', 'address')


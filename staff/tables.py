import django_tables2 as tables
from .models import Staff
import itertools
from django.utils.html import format_html
from students.models import Student
from django_tables2 import A
from django.utils.translation import ugettext_lazy as _


class StaffTable(tables.Table):
    row_number = tables.Column(empty_values=(), verbose_name="No.")
    edit_staff = tables.TemplateColumn('<a href=" {% url "institutions:edit_institution_staff" username=record.staffuser  %} "  ><center><span class="fas fa-edit"></span></center></a>')
    delete_staff = tables.TemplateColumn('<a href=" {% url "institutions:delete_institution_staff" username=record.staffuser  %}" ><center><span class="fas fa-trash-alt"></span></center></a>')
    email_student = tables.Column(accessor='staffuser.email',
                          verbose_name='Email')
    first_name = tables.Column(accessor='staffuser.first_name',
                          verbose_name='First Name')
    last_name = tables.Column(accessor='staffuser.last_name',
                          verbose_name='Last Name')
    
    def __init__(self, *args, **kwargs):
        super(StaffTable, self).__init__(*args, **kwargs)
        self.counter = itertools.count()

    def render_row_number(self):
        return '%d' % (int(next(self.counter))+1)

    

    class Meta:
        model = Staff
        # add class="paleblue" to <table> tag
        exclude = ('id', 'deleted', 'user_type', 'institute', 'created', 'updated', 'allowregistration', )
        attrs = {'class': 'paleblue'}
        # fields = ('row_number', 'institute',)
        sequence = ('row_number', 'staffuser', 'first_name', 'last_name', 'email_student', 'user_type', 'deleted')



class StudentTable(tables.Table):
    row_number = tables.Column(empty_values=(), verbose_name="No.")
    first_name = tables.Column(accessor='studentuser.first_name',
                               verbose_name='First Name')
    last_name = tables.Column(accessor='studentuser.last_name',
                              verbose_name='Last Name')
    email = tables.Column(accessor='studentuser.email',
                          verbose_name='Mail Address')
    
    edit_student = tables.TemplateColumn('<a href=" {% url "staff:student_edit_by_staff" upk=record.pk  %} "><center><span class="fas fa-edit "></span></center></a>', verbose_name="Edit")
    delete_student = tables.TemplateColumn('<a href=" {% url "staff:delete_institution_staff_student" username=record.studentuser  %} "><center><span class="fas fa-trash-alt"></span></center></a>', verbose_name="Delete")
    #student_fees = tables.TemplateColumn('<a href=" {% url "staff:fees:manage_fees_installment" pk=record.id  %} ">Installment</a>', verbose_name="Fees")
    Approval = tables.TemplateColumn(
        '<a href=" {% url "staff:student_activate_deactivate" pk=record.id  %} ">'
        '{% if record.studentuser.is_active %}'
        'Deactivate'
        '{% else %}'
        'Activate'
        '{% endif %}'
        '</a>',order_by="studentuser.is_active"
        )
    standard = tables.Column(accessor='standard', verbose_name=_('Std.'))
    staffuser = tables.Column(accessor='staffuser', verbose_name=_('Under Professor'))
	
    def __init__(self, *args, **kwargs):
        super(StudentTable, self).__init__(*args, **kwargs)
        self.counter = itertools.count()

    def render_row_number(self):
        return ' %d' % next(self.counter)

    def render_first_name(self,value):
        return value
    
    def render_last_name(self,value):
        return value
    
    def render_email(self,value):
        return value
        
    
    class Meta:
        model = Student
        sequence = ('row_number', 'studentuser','first_name','last_name','email', 'staffuser',  )
        # add class="paleblue" to <table> tag 
        attrs = {'class': 'paleblue'}
        # fields = ('row_number', 'institute',)
        exclude = ('id', 'deleted', 'last_login', 'created', 'updated', 'user_type',)


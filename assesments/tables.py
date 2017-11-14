import django_tables2 as tables
import itertools
from django.utils.html import format_html
from .models import Assesment
from django_tables2 import A




class AssesmentTable(tables.Table):
    row_number = tables.Column(empty_values=(),
                                verbose_name='Row')
    
    edit_assesment = tables.TemplateColumn('<a href=" ">Edit</a>')
    delete_assesment = tables.TemplateColumn('<a href=" ">Delete</a>')
    manage_assesment = tables.TemplateColumn('<a href=" ">Manage</a>')
    
    def __init__(self, *args, **kwargs):
        super(AssesmentTable, self).__init__(*args, **kwargs)
        self.counter = itertools.count()

    def render_row_number(self):
        return '%d' % next(self.counter)

    def render_brief(self,value):
        return (value[:75] + '..') if len(value) > 75 else value
   
    class Meta:
        model = Assesment
        sequence = ('row_number', 'header','brief','start_time','end_time','exam_start_type', 'total_exam_duration','total_question','privilege','is_exam_active','expired_on')
        # add class="paleblue" to <table> tag 
        attrs = {'class': 'paleblue'}
        # fields = ('row_number', 'institute',)
        exclude = ('id', 'deleted_at','deleted_by','created_by','updated_by','type')

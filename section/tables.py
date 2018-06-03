import django_tables2 as tables
from .models import Section
import itertools


class ManageSectionTable(tables.Table):
    row_number = tables.Column(empty_values=(),
                                verbose_name='No.')
    
    edit_section= tables.TemplateColumn('<a href="{% url "staff:assesments:section:edit_question_section" pk=record.pk %}">Edit</a>')
    delete_section= tables.TemplateColumn('<a href="{% url "staff:assesments:section:delete_question_section" pk=record.pk %}">Delete</a>')
    manage_section= tables.TemplateColumn('<a href="{% url "staff:assesments:section:manage_question_section" pk=record.pk %}">Manage</a>')
    
    def __init__(self, *args, **kwargs):
        super(ManageSectionTable, self).__init__(*args, **kwargs)
        self.counter = itertools.count()
    
    def render_row_number(self):
        return '%d' % next(self.counter)
    
    class Meta:
        model = Section
        attrs = {'class': 'paleblue'}
        sequence = ('row_number','name','linked_assessment')
        exclude = ('id')
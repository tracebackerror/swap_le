import django_tables2 as tables
from .models import Section
import itertools


class ManageSectionTable(tables.Table):
    
    
    edit= tables.TemplateColumn('<div class="col-md-12"><a alt="edit" class="btn-link"  href="{% url "staff:assesments:section:edit_question_section" assesmentid=record.linked_assessment.pk pk=record.pk %} "><center><span class="fas fa-cogs "></span></center></a> </div> ', verbose_name=" ", orderable=False)
    action= tables.TemplateColumn('<div class="col-md-12"> <a href="{% url "staff:assesments:section:delete_question_section" pk=record.pk %} "><center><span class="fas fa-trash-alt"></span></center></a></div></div>', verbose_name=" ", orderable=False)
    
    #manage_section= tables.TemplateColumn('<a href="{% url "staff:assesments:section:manage_question_section" pk=record.pk assesmentid=record.linked_assessment.pk %}">Manage</a>')
    
    def __init__(self, *args, **kwargs):
        super(ManageSectionTable, self).__init__(*args, **kwargs)
        self.counter = itertools.count()
    
    
    class Meta:
        model = Section
        attrs = {'class': 'paleblue'}
        sequence = ('name','linked_assessment')
        exclude = ('id', 'linked_assessment')
import django_tables2 as tables
import itertools
from django.utils.html import format_html
from .models import Assesment, Question, Result
from django_tables2 import A

from django.core.urlresolvers import reverse
class ResultTable(tables.Table):
    row_number = tables.Column(empty_values=(),
                                verbose_name='No.')
    
    review_sqa = tables.LinkColumn('reviewsqa', text='Review Descriptive Answer')
    #review_sqa = tables.TemplateColumn('<a href="{% url "staff:assesments:assesment_manage_review_sqa_question" assesmentid=self.request.GET.assesmentid %}">Review Descriptive Answer</a>')
    result_report = tables.TemplateColumn('<a href="{% url "staff:assesments:assessment_result_by_staff" pk=record.pk %}">View</a>')

    def render_review_sqa(self, record):
        url = reverse('staff:assesments:assesment_manage_review_sqa_question',kwargs={'assesmentid': self.assesmentid})
        return format_html('<a href="{}">{}</a>', url, 'Review Descriptive Answer')
        
    def render_registered_user(self, record):
        reg_user = record.registered_user.get_name_registered_student()
        return format_html('{}'.format(reg_user))
    
    def __init__(self, *args, **kwargs):
        super(ResultTable, self).__init__(*args)
        self.counter = itertools.count()
        self.assesmentid = kwargs.get('assesmentid',None)
    
    def render_row_number(self):
        return '%d' % next(self.counter)
    
    class Meta:
        model = Result
        attrs = {'class': 'paleblue'}
        sequence = ('row_number',)
        exclude = ('id', 'deleted_at','deleted_by','created_by','updated_by','type','assesment','created','updated',)

class QuestionTable(tables.Table):
    row_number = tables.Column(empty_values=(),
                                verbose_name='No.')
    
    delete_question = tables.TemplateColumn('<a href="{% url "staff:assesments:assessment_question_delete" questionid=record.pk %}">Delete</a>')
    
    def __init__(self, *args, **kwargs):
        super(QuestionTable, self).__init__(*args, **kwargs)
        self.counter = itertools.count()
    
    def render_row_number(self):
        return '%d' % next(self.counter)
        
    
    class Meta:
        model = Question
        attrs = {'class': 'paleblue'}
        sequence = ('row_number',)
        exclude = ('id', 'deleted_at','deleted_by','created_by','updated_by','created','updated', 'assesment_linked', 'question_image' )

class AssesmentTable(tables.Table):
    row_number = tables.Column(empty_values=(),
                                verbose_name='Row')
    
    edit_assesment = tables.TemplateColumn('<a href=" {% url "staff:assesments:assessment_edit_by_staff" assesmentid=record.id  %} "><center><span class="glyphicon glyphicon-edit ">Edit</span></center></a></a>')
    delete_assesment = tables.TemplateColumn('<a href=" {% url "staff:assesments:assessment_delete_by_staff" assesmentid=record.id  %} "><center><span class="glyphicon glyphicon-remove">Delete</span></center></a>')
    manage_assesment = tables.TemplateColumn('<a href=" {% url "staff:assesments:assessment_manage_by_staff" assesmentid=record.id  %} ">Manage</a>')
    
    #manage_assesment = tables.TemplateColumn('<form method="GET"  action="{%  url "staff:assesments:assessment_manage_by_staff" %}">  {% csrf_token %} <input type="hidden" name="examid" value={{record.id }}> <input class="btn btn-dark" type="submit" value="Manage"> </form>')
    
    def __init__(self, *args, **kwargs):
        super(AssesmentTable, self).__init__(*args, **kwargs)
        self.counter = itertools.count()

    def render_row_number(self):
        return '%d' % next(self.counter)

    def render_brief(self,value):
        return (value[:75] + '..') if len(value) > 75 else value
   
    class Meta:
        model = Assesment
        sequence = ('row_number', 'header','brief','exam_start_date_time', 'passing_marks','privilege')
        # add class="paleblue" to <table> tag 
        attrs = {'class': 'paleblue'}
        # fields = ('row_number', 'institute',)
        exclude = ('id', 'deleted_at','deleted_by','created_by','updated_by','type','exam_start_type','expired_on','is_exam_active')



class StudentAssesmentTable(tables.Table):
    row_number = tables.Column(empty_values=(),
                                verbose_name='No.')
    
    take_assesment = tables.TemplateColumn('<form method="POST"  action=".">  {% csrf_token %} <input type="hidden" name="examid" value={{record.id }}> <input type="submit" class="btn btn-dark" value="Take Exam"> </form>')
    
    '''
    completed = tables.BooleanColumn(empty_values=(),
                                verbose_name='Completed')
    
    '''
    def __init__(self, *args, **kwargs):
        super(StudentAssesmentTable, self).__init__(*args, **kwargs)
        self.counter = itertools.count()

    def render_row_number(self):
        return '%d' % next(self.counter)
    
    
    '''
    def render_completed(self,value):
       return '%s' % value
    
    def render_total_exam_duration(self,value):
        return '%s' % value
    '''    
    
    def render_brief(self,value):
        return (value[:75] + '..') if len(value) > 75 else value
    
   
    class Meta:
        model = Assesment
        sequence = ('row_number', 'header','exam_start_date_time','passing_marks','privilege','expired_on')
        # add class="paleblue" to <table> tag 
        attrs = {'class': 'paleblue'}
        # fields = ('row_number', 'institute',)
        exclude = ('id', 'deleted_at','brief','deleted_by','created_by','updated_by','type','exam_start_type', 'polymorphic_ctype','created','updated','slug','is_exam_active')

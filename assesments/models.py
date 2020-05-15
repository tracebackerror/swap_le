from django.db import models
from django.utils.text import slugify
from django.utils import timezone

from utility.mixin import MetaInformationMixin, SoftDeletionModelMixin
from students.models import Student
from datetime import datetime, timedelta

from autoslug import AutoSlugField
from meta.models import ModelMeta
from taggit.managers import TaggableManager
from django.utils.html import strip_tags

class AssesmentManager(models.Manager):
    def get_queryset(self):
        return super(AssesmentManager, self).get_queryset()\
                .filter(deleted='N')


class Assesment(MetaInformationMixin, SoftDeletionModelMixin, ModelMeta):
    ASSESMENT_START_TYPE_CHOICES = (
        ('auto', 'Automatic'),
        ('manual', 'Manually'),
        )
    
    ASSESMENT_PRIVILEGE_CHOICES = (
        ('public', 'Public'),
        ('private', 'Private'),
        ('open', 'Open - Visible to Entire World'),
        )
    
    #objects = models.Manager()  # The Default Manager
    #active = AssesmentManager()  # Our custom manager


    header = models.CharField(max_length=150)
    slug = AutoSlugField(populate_from='header', unique = True)
    '''
    slug = models.SlugField(max_length=140,
                            unique=True,
                            blank=True)
    '''
    brief = models.TextField()
    exam_start_date_time = models.DateTimeField(default=datetime.now)
    
    exam_start_type = models.CharField(max_length=14,
                                       choices=ASSESMENT_START_TYPE_CHOICES,
                                       default='auto')
    

    
    passing_marks = models.IntegerField(default=0)
    
    privilege = models.CharField(max_length=14,
                                       choices=ASSESMENT_PRIVILEGE_CHOICES,
                                       default='public')
    
   
    is_exam_active = models.BooleanField(default=True, blank=True)
    expired_on = models.DateTimeField(default=datetime.now)
    
    
    
    type = models.CharField(max_length=10, default="assessment", editable=False)
    #deleted = models.CharField(max_length=1, default="N")

    subscriber_users = models.ManyToManyField(Student, blank=True)
    
    duration_hours = models.IntegerField(null=True)
    duration_minutes = models.IntegerField(null=True)
    
    tags = TaggableManager()
    
    _metadata = {
        'title': 'header',
        'description': 'brief',
        'author': 'get_assessment_author'
        
    } 
    
    def get_assessment_author(self):
        if self.created_by:
            return self.created_by.get_full_name()
    class Meta:
        ordering = ('created',)
        
        
    def __str__(self):
        return 'Assesment - {}'.format(self.header)
    
    def _get_unique_slug(self):
        slug = slugify(self.header)
        unique_slug = slug
        num = 1
        while Assesment.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug
 
    def save(self, *args, **kwargs):
        '''
        if not self.slug:
            self.slug = self._get_unique_slug()
        ''' 
        if self.pk is None and self.created_by is None:
            self.created_by = user
        elif self.updated_by is None:
            self.updated_by = user
        super(Assesment, self).save()






class Question(MetaInformationMixin, SoftDeletionModelMixin):
    QUESTION_TYPE_CHOICES = (
        ('mcq', 'Multiple Choice'),
        ('scq', 'Single Choice'),
        ('sqa', 'Text Answer'),
        )
    
    #objects = models.Manager()  # The Default Manager
    #active = AssesmentManager()  # Our custom manager



    question_text = models.TextField()
    question_image = models.TextField(blank=True,null=True, editable=True)

    length_size = 250    
    option_one = models.TextField(max_length=length_size,
                                    blank=True,
                                    null=True)
    option_two = models.TextField(max_length=length_size,
                                    blank=True,
                                    null=True)
    option_three = models.TextField(max_length=length_size,
                                        blank=True,
                                        null=True)
    option_four = models.TextField(max_length=length_size,
                                    blank=True,
                                    null=True)
    option_five = models.TextField(max_length=length_size,
                                    blank=True,
                                    null=True)
    '''
    question_slug = models.SlugField(max_length=140,
                            unique=True,
                            blank=True)
    
    
    '''
   
    question_type = models.CharField(max_length=14,
                                       choices=QUESTION_TYPE_CHOICES,
                                       default='scq')
    
    
    brief_answer = models.TextField(blank=True,
                                    null=True)
    
    max_marks = models.IntegerField()
    correct_options = models.CharField(max_length = 150,
                                       blank=True,
                                       null=True)
    
    
    assesment_linked = models.ForeignKey(Assesment,
                                                null=True,
                                                on_delete=models.CASCADE)
    
    
    def __str__(self):
        data_temp = strip_tags(self.question_text).replace("&nbsp;", "")
        data = (data_temp[:150] + '..') if len(data_temp) > 75 else data_temp
        return data
    
    
class Result(MetaInformationMixin, SoftDeletionModelMixin):
   
    #objects = models.Manager()  # The Default Manager
    #active = AssesmentManager()  # Our custom manager

    assesment = models.ForeignKey(Assesment, on_delete=models.CASCADE)
    registered_user = models.ForeignKey(Student, on_delete=models.CASCADE)
    #attempt_number = models.IntegerField(default=10) --FUTURE IMPL
    
    exam_taken_date_time = models.DateTimeField(default=timezone.now)
    
    total_question = models.IntegerField(default=0)
    total_attempted = models.IntegerField(default=0)
    
    #total_time_taken = models.TimeField(null=True)
    total_marks = models.IntegerField(default=0)
    obtained_marks = models.IntegerField(default=0)
    
    publish_result = models.BooleanField(default=True)
    result_passed = models.BooleanField(default=False)
    type = models.CharField(max_length=10, default="result", editable=False)
    
    assesment_submitted = models.BooleanField(default=False)
    #deleted = models.CharField(max_length=1, default="N")

    
        
    def __str__(self):
        return 'Result : {}-{}'.format(self.assesment,self.registered_user)
    
   
 
   

class Answer(MetaInformationMixin, SoftDeletionModelMixin):
    '''
    QUESTION_TYPE_CHOICES = (
        ('mcq', 'Multiple Choice'),
        ('scq', 'Single Choice'),
        ('sqa', 'Text Answer'),
        )
    '''
    #objects = models.Manager()  # The Default Manager
    #active = AssesmentManager()  # Our custom manager


    for_result = models.ForeignKey(Result, on_delete=models.CASCADE)
    for_question = models.ForeignKey(Question, on_delete=models.CASCADE)

    length_size = 250    
   
    opted_choice =  models.TextField(max_length=length_size)
    written_answer = models.TextField(null=True, blank=True)
    alloted_marks = models.FloatField(max_length=length_size)
    
    def __str__(self):
        data = (self.for_question.question_text[:150] + '..') if len(self.for_question.question_text) > 75 else self.for_question.question_text
        return 'Question - {}'.format(data)
     

    
    
    
    
    
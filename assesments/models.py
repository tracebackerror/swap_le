from django.db import models
from django.utils.text import slugify
from django.utils import timezone

from utility.mixin import MetaInformationMixin, SoftDeletionModelMixin
from students.models import Student


class AssesmentManager(models.Manager):
    def get_queryset(self):
        return super(AssesmentManager, self).get_queryset()\
                .filter(deleted='N')


class Assesment(MetaInformationMixin, SoftDeletionModelMixin):
    ASSESMENT_START_TYPE_CHOICES = (
        ('auto', 'Automatic'),
        ('manual', 'Manually'),
        )
    
    ASSESMENT_PRIVILEGE_CHOICES = (
        ('public', 'Public'),
        ('private', 'Private'),
        ('protected', 'Protected'),
        )
    
    #objects = models.Manager()  # The Default Manager
    #active = AssesmentManager()  # Our custom manager


    header = models.CharField(max_length=150)
    slug = models.SlugField(max_length=140,
                            unique=True,
                            blank=True)
    brief = models.TextField()
    start_time = models.DateTimeField(default=timezone.now,
                                       verbose_name="Start Timing")
    end_time = models.DateTimeField(default=timezone.now)
    exam_start_type = models.CharField(max_length=14,
                                       choices=ASSESMENT_START_TYPE_CHOICES,
                                       default='auto')
    

    total_exam_duration = models.TimeField(null=True)
    passing_marks = models.IntegerField(default=0)
    
    privilege = models.CharField(max_length=14,
                                       choices=ASSESMENT_PRIVILEGE_CHOICES,
                                       default='private')
    
   
    is_exam_active = models.BooleanField(default=True)
    expired_on = models.DateTimeField()
    
    
    
    type = models.CharField(max_length=10, default="assessment", editable=False)
    #deleted = models.CharField(max_length=1, default="N")

    subscriber_users = models.ManyToManyField(Student)
    
    
        
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
        if not self.slug:
            self.slug = self._get_unique_slug()
        
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
                                                null=True)
    
    
    def __str__(self):
        return 'Question - {}'.format(self.question_text)
    
    
class Result(MetaInformationMixin, SoftDeletionModelMixin):
   
    #objects = models.Manager()  # The Default Manager
    #active = AssesmentManager()  # Our custom manager

    assesment = models.ForeignKey(Assesment)
    registered_user = models.ForeignKey(Student)
    #attempt_number = models.IntegerField(default=10) --FUTURE IMPL
    
    exam_taken_date_time = models.DateTimeField(default=timezone.now)
    
    total_question = models.IntegerField(default=0)
    total_attempted = models.IntegerField(default=0)
    
    #total_time_taken = models.TimeField(null=True)
    total_marks = models.IntegerField(default=0)
    obtained_marks = models.IntegerField(default=0)
    
    publish_result = models.BooleanField(default=False)
    result_passed = models.BooleanField(default=False)
    type = models.CharField(max_length=10, default="result", editable=False)
    
    assesment_submitted = models.BooleanField(default=False)
    #deleted = models.CharField(max_length=1, default="N")

   
    def __str__(self):
        return 'Result : {}-{}-{}'.format(self.assesment,self.registered_user)
    
   
 
   

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


    for_result = models.ForeignKey(Result)
    for_question = models.ForeignKey(Question)

    length_size = 250    
   
    opted_choice =  models.TextField(max_length=length_size)
    written_answer = models.TextField()
    alloted_marks = models.FloatField(max_length=length_size)
     

    
    
    
    
    
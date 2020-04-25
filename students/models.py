from django.db import models
from django.utils import timezone
from institutions.models import Institutions
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.
from staff.models import Staff


class StudentManager(models.Manager):
    def get_queryset(self):
        return super(StudentManager, self).get_queryset()\
                .filter(deleted='N')


class Student(models.Model):
    STUDENT_STATUS_CHOICES = (
        ('inac', 'Inactive'),
        ('acti', 'Active'),
        ('dele', 'Deleted'),
        )

    objects = models.Manager()  # The Default Manager
    active = StudentManager()  # Our custom manager

    studentuser = models.OneToOneField(settings.AUTH_USER_MODEL,
                                        on_delete=models.CASCADE,
                                        null=True,
                                        verbose_name='Student Id'
                                        )
    staffuser = models.ForeignKey(Staff,
                                  on_delete=models.CASCADE,
                                  null=True,
                                  verbose_name='Staff Id'
                                  )
    
    
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Created On')
    updated = models.DateTimeField(auto_now=True,
                                   verbose_name='Last Updated On')
    
    user_type = models.CharField(max_length=10,
                                 default="student",
                                 editable=False,
                                 verbose_name='Privilege')
    deleted = models.CharField(max_length=1,
                               default="N",
                               verbose_name='Deactive')

    last_login =  models.DateTimeField(auto_now=True)
    
    standard = models.CharField(max_length=20,null=True)
    address = models.TextField(null=True)
    student_contact_no = models.CharField(null=True, max_length=20)
    parent_contact_no = models.CharField(null=True, blank=True, max_length=20)
    gender = models.CharField(max_length = 10,null=True)
    
    
    class Meta:
        ordering = ('created',)
        
    def get_student_name_for_staff(self):
        return "{} {} ({}) <- {}".format(self.studentuser.first_name, self.studentuser.last_name, self.studentuser.username, self.staffuser.staffuser.username)
    
    def get_name_registered_student(self):
        return "{},{} ({})".format(self.studentuser.first_name.title(), self.studentuser.last_name.title(), self.studentuser.username)
        
    def __str__(self):
       return self.get_name_registered_student()

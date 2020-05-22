from django.db import models
from django.utils import timezone
from institutions.models import Institutions
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.
from staff.models import Staff
from utility.swaple_constants import *

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
    
    def get_all_standard(self):
        return COURSE_CHOICES
    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in Student._meta.fields]
    
    class Meta:
        ordering = ('created',)
        
    def get_student_name_for_staff(self):
        return "{} {} ({}) <- {}".format(self.studentuser.first_name, self.studentuser.last_name, self.studentuser.username, self.staffuser.staffuser.username)
    
    def get_name_registered_student(self):
        if self.studentuser.first_name and self.studentuser.last_name and self.standard:
            return "{},{}-{}".format(self.studentuser.first_name, self.studentuser.last_name, self.standard).title()
        elif self.studentuser.first_name and self.studentuser.last_name:
            return "{},{}-Empty".format(self.studentuser.first_name, self.studentuser.last_name).title()
        else:
            return "{}".format(self.studentuser)
        
    def __str__(self):
       return self.get_name_registered_student()

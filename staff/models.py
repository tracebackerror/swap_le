from django.db import models
from django.utils import timezone
from institutions.models import Institutions
from django.conf import settings
from pyexpat import model
# Create your models here.


class StaffManager(models.Manager):
    def get_queryset(self):
        return super(StaffManager, self).get_queryset()\
	            .filter(deleted='N')


class Staff(models.Model):
    STAFF_STATUS_CHOICES = (
        ('inac', 'Inactive'),
        ('acti', 'Active'),
        ('dele', 'Deleted'),
        )

    objects = models.Manager()  # The Default Manager
    active = StaffManager()  # Our custom manager

    staffuser = models.OneToOneField(settings.AUTH_USER_MODEL,
                                      on_delete=models.CASCADE,
                                      verbose_name="Username"
                                      )
    institute = models.ForeignKey(Institutions, related_name='staffinstitute',
                                  on_delete=models.CASCADE)
    allowregistration = models.BooleanField(default=True)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    user_type = models.CharField(max_length=10, default="staff", editable=False)
    deleted = models.CharField(max_length=1, default="N")

    
    class Meta:
        ordering = ('created',)
        permissions = (
            ("is_staff", "Friendly permission description"),
        )
    def __str__(self):
        return 'Staff - {} Of Institute - {}'.format(self.staffuser.username, self.institute.institute_name)
        
        
    def get_staff_name(self):
        return "{} {} ({})".format(self.staffuser.first_name.strip(), self.staffuser.last_name.strip(), self.staffuser.username)
        
class StudentEnquiry(models.Model):
    created_by=models.ForeignKey(Staff,on_delete=models.CASCADE)
    full_name=models.CharField(max_length=100)
    parent_name=models.CharField(max_length=50)
    scl_clg_name=models.CharField(max_length=50)
    std=models.CharField(max_length=10)
    academic_y=models.CharField(max_length=50)
    contact=models.IntegerField()
    

    def __str__(self):
        return "{0}({1})".format(self.full_name,self.created_by)
    
    
    
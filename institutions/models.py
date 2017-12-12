from django.db import models
from django.utils import timezone
from django.conf import settings

# Create your models here.

class InstitutionsManager(models.Manager):
    def get_queryset(self):
        return super(InstitutionsManager, self).get_queryset()\
	            .filter(institute_status='acti').filter(deleted='N')

class Institutions(models.Model):
	
    objects = models.Manager() # The Default Manager
    active = InstitutionsManager() # Our custom manager
	
    INSTITUTION_STATUS_CHOICES = (
        ('inac', 'Inactive'),
        ('acti', 'Active'),
        ('pend', 'Pending'),
        ('dele', 'Deleted'),
        ) 
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, editable=True,verbose_name='Institute User Name',on_delete=models.CASCADE)
    institute_name = models.CharField(max_length=45, null=False)
    institute_contact_mobile = models.CharField( max_length=13, null = False)
    institute_contact_landline = models.CharField( max_length=13, null = True)
    institute_address = models.CharField(max_length=200, null = False)
    institute_city = models.CharField(max_length=20, null = False)
    institute_state = models.CharField(max_length=20, null = False)
    institute_country = models.CharField(max_length=20, null = False)

    institute_created = models.DateTimeField(auto_now_add=True)
    institute_last_updated = models.DateTimeField(auto_now=True)
    institute_password_last_updated = models.DateTimeField(auto_now_add=True)
    
    institute_status =  models.CharField(max_length=4,choices=INSTITUTION_STATUS_CHOICES,default='pend')
    user_type = models.CharField(max_length=11, default="institution", editable=False)
    deleted = models.CharField(max_length=1, default="N", editable=False)

    class Meta:
        ordering = ('-institute_last_updated','-institute_created')
    
    def __str__(self):
        detailed = "%s - %s - %s - %s" % (str(self.institute_name),str(self.institute_city),str(self.institute_state),str(self.institute_country)) 
        return  detailed
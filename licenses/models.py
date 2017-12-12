from django.db import models
from django.utils import timezone
from institutions.models import Institutions
# Create your models here.

class License(models.Model):
    LICENSE_STATUS_CHOICES = (
        ('inac', 'Inactive'),
        ('acti', 'Active'),
        ('expi', 'Expired'),
        ) 

    li_key = models.CharField(max_length=45, null = False)
    li_expiration_date = models.DateTimeField(default=timezone.now)
    li_created = models.DateTimeField(auto_now_add=True)
    li_updated = models.DateTimeField(auto_now=True)
    li_max_staff = models.IntegerField(default=0)
    li_max_students = models.IntegerField(default=0)
    li_max_assesments = models.IntegerField(default=0)
	
    li_institute = models.ForeignKey(Institutions, related_name='licensed_institute', null= True,on_delete=models.CASCADE)

    li_current_staff = models.IntegerField(default=0)
    li_current_students = models.IntegerField(default=0)
    li_current_assesments =  models.IntegerField(default=0)
    
    li_current_status =  models.CharField(max_length=4,choices=LICENSE_STATUS_CHOICES,default='inac')
 
    class Meta:
        ordering = ('-li_current_assesments',)

    
    def __str__(self):
        return str(self.li_key) + " - " + str(self.li_current_status) 
from django.db import models
from institutions.models import Institutions
from staff.models import Staff
from students.models import Student

# Create your models here.

class LibraryAsset(models.Model):
    ASSET_TYPE_CHOICES = (
        ('book ','BOOK'),
        ('cd','CD'),
        ('dvd','DVD')
        )
    
    for_institution = models.ForeignKey(Institutions,on_delete=models.CASCADE)
    name = models.CharField(max_length=50,null=True)
    asset_type = models.CharField(max_length=10,choices=ASSET_TYPE_CHOICES)
    asset_unique_code = models.CharField(max_length=50, unique=True)
    asset_description = models.TextField()
    availability = models.BooleanField(default = True)
    created_by = models.ForeignKey(Staff,on_delete=models.CASCADE)
    
    def __str__(self):
        return "{0}-{1}".format(self.created_by, self.asset_unique_code)
    

class AssetHistory(models.Model):
    asset_id = models.ForeignKey(LibraryAsset,on_delete=models.CASCADE)
    student_id = models.ForeignKey(Student,on_delete=models.CASCADE,null=True)
    checked_in = models.DateTimeField(null=True)
    checked_in_user_id = models.ForeignKey(Staff,on_delete=models.CASCADE,null=True)
    checked_out = models.DateTimeField(null=True)
    
    def __str__(self):
        return "{0}-{1}".format(self.checked_in_user_id, self.asset_id.asset_unique_code)
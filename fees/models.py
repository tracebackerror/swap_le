from django.db import models
from students.models import Student

# Create your models here.

class FeesInstallment(models.Model):
    student_id = models.ForeignKey(Student,on_delete=models.CASCADE)
    amount = models.FloatField()
    day = models.IntegerField()
    month = models.CharField(max_length = 3)
    year = models.IntegerField()
    paid = models.BooleanField()
    
    def  __str__(self):
        return "{0}-{1}".format(self.student_id.studentuser.username,self.month)
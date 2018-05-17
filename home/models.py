from django.db import models

# Create your models here.

class ContactUs(models.Model):
    name=models.CharField(max_length=30)
    email=models.EmailField()
    subject=models.CharField(max_length=50)
    message=models.CharField(max_length=140)
    
    def __str__(self):
        return "{0}({1})".format(self.name,self.subject)
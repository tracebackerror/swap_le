from django.db import models
from assesments.models import Assesment

# Create your models here.

class Section(models.Model):
    name = models.CharField(max_length = 50)
    linked_assessment = models.ForeignKey(Assesment,on_delete = models.CASCADE)
    
    def __str__(self):
        return self.name
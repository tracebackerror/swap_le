from django.db import models
from assesments.models import Assesment,Question

# Create your models here.

class Section(models.Model):
    name = models.CharField(max_length = 50)
    linked_assessment = models.ForeignKey(Assesment,on_delete = models.CASCADE)
    
    def __str__(self):
        return self.name
    

class SectionQuestionMapping(models.Model):
    for_section = models.ForeignKey(Section,on_delete = models.CASCADE)
    for_question = models.ForeignKey(Question,on_delete = models.CASCADE) 
    
    def __str__(self):
        return self.for_question.question_text
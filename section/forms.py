from django import forms
from .models import Section
from assesments.models import Assesment, Question

class AddQuestionSectionForm(forms.ModelForm):
    name = forms.CharField(widget = forms.TextInput(),required = True, label="Section Name")
    
    
    def __init__(self, *args, **kwargs):
    
        #user = kwargs.pop('user', None)
        super(AddQuestionSectionForm, self).__init__(*args, **kwargs)
        #user_profile = UserProfile.objects.get(user=user)
        
    class Meta():
        model = Section
        fields = ['name', ]
        widgets = {
            'for_question': forms.CheckboxSelectMultiple(
                                       attrs={}
                                    ),
            
        }
        
class EditQuestionSectionForm(forms.ModelForm):
    name = forms.CharField(widget = forms.TextInput(),required = True, label="Section Name")
    
    for_question = forms.ModelMultipleChoiceField(queryset = Question.objects.filter(assesment_linked__pk=1),
                                                      )
    def __init__(self, *args, **kwargs):
    
        #user = kwargs.pop('user', None)
        super(EditQuestionSectionForm, self).__init__(*args, **kwargs)
        #user_profile = UserProfile.objects.get(user=user)
        
        self.fields["for_question"].queryset = Question.objects.filter(assesment_linked = kwargs['instance'].linked_assessment)
    class Meta():
        model = Section
        fields = ['name', 'for_question']
        widgets = {
            'for_question': forms.CheckboxSelectMultiple(
                                       attrs={}
                                    ),
            
        }
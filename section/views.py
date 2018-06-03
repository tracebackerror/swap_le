from django.shortcuts import *
from .models import Section
from django.views.generic import FormView,DeleteView,UpdateView,ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AddQuestionSectionForm
from .models import Section,SectionQuestionMapping
from assesments.models import Assesment,Question
from django.urls import reverse_lazy,reverse
from django.contrib import messages

# Create your views here.

class AddQuestionSection(FormView):
    model = Section
    template_name="section/add_question_section.html"
    success_url = 'staff:assesments:assessment_manage_by_staff'
    form_class = AddQuestionSectionForm
    context_object_name = "form"
    login_url=reverse_lazy('staff:login')
    
    def form_valid(self, form,**kwargs):
        assesmentid = self.kwargs.get('assesmentid')
        linked_assessment = Assesment.objects.get(id = assesmentid)
        name  = form.cleaned_data['name']
        Section.objects.create(name=name,linked_assessment=linked_assessment)
        messages.add_message(self.request, messages.SUCCESS, 'Question Section Created!')
        return HttpResponseRedirect(self.get_success_url(assesmentid))
    
    def get_success_url(self,assesmentid):
        return reverse(self.success_url, kwargs={'assesmentid': assesmentid})


 
class DeleteQuestionSection(LoginRequiredMixin,DeleteView):
    model = Section
    template_name="section/delete_question_section.html"
    success_url =  reverse_lazy('staff:assesments:manage_all_assesment')
    context_object_name = "Section"
    pk_url_kwarg = 'pk'
    login_url=reverse_lazy('staff:login')
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.add_message(self.request, messages.SUCCESS, 'Deleted Question Section Successfully!')
        return HttpResponseRedirect(self.success_url)
    
    
class EditQuestionSection(LoginRequiredMixin,UpdateView):
    model = Section
    template_name="section/edit_question_section.html"
    success_url =  reverse_lazy('staff:assesments:manage_all_assesment')
    form_class = AddQuestionSectionForm
    context_object_name = "form"
    login_url=reverse_lazy('staff:login')
     
    
    def form_valid(self, form):
        if super(EditQuestionSection,self).form_valid(form):
            form.save()
            messages.add_message(self.request, messages.SUCCESS, 'Updated Question Section Successfully!')
        return HttpResponseRedirect(self.success_url)
    
    

class ManageQuestionSection(LoginRequiredMixin,ListView):
    model = Section
    template_name="section/manage_question_section.html"
    context_object_name = "model"
    success_url =  reverse_lazy('staff:assesments:manage_all_assesment')
    login_url=reverse_lazy('staff:login')

    def get_queryset(self,**kwargs):
        pk = self.kwargs.get('pk')
        section_obj = Section.objects.get(id = pk)
        assessment_obj = Assesment.objects.filter(id=section_obj.linked_assessment.id)
        queryset = Question.objects.filter(assesment_linked = assessment_obj)
        return queryset
    
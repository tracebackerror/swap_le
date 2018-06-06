from django.shortcuts import *
from .models import Section
from django.views.generic import FormView,DeleteView,UpdateView,ListView,View
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
    
    

class ManageQuestionSection(LoginRequiredMixin,View):
    model = Question
    template_name="section/manage_question_section.html"
    success_url =  reverse_lazy('staff:assesments:manage_all_assesment')
    context_object_name = "model"
    login_url=reverse_lazy('staff:login')

    def get_queryset(self,**kwargs):
        pk = self.kwargs.get('pk')
        section_obj = Section.objects.get(id = pk)
        assessment_obj = Assesment.objects.filter(id=section_obj.linked_assessment.id)
        queryset = Question.objects.filter(assesment_linked = assessment_obj)
        return queryset
              
    def post(self, request, *args, **kwargs):
        question_id = self.request.POST['question_id']
        pk = self.kwargs.get('pk')
        for_section = Section.objects.get(id = pk)
        
        qsmapping = SectionQuestionMapping.objects.filter(for_section = for_section)
        qsmapping_q_id = []
        for i in qsmapping:
            qsmapping_q_id.append(i.for_question.id)
        print(qsmapping_q_id)
        print(question_id.split(','))
        
        for i in question_id.split(','):
            for_question = Question.objects.get(id = i)
            already_mapping = SectionQuestionMapping.objects.filter(for_section = for_section,for_question = for_question)
            #add data code
            if already_mapping :
                print("already exists")
            else:
                SectionQuestionMapping.objects.create(for_section = for_section,for_question = for_question)
                
        #delete data code start
            if int(i) in qsmapping_q_id:
                qsmapping_q_id.remove(int(i))
        
        for i in qsmapping_q_id:
            SectionQuestionMapping.objects.get(for_question__id = i).delete()
        #delete data code end
            
        messages.add_message(self.request, messages.SUCCESS, 'Questions Successfully Managed in Section!')
        
        return HttpResponseRedirect(self.success_url)
        
                
    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data(object_list=self.object_list)
        return self.render_to_response(context)
    
    def get_context_data(self, **kwargs):
        queryset = kwargs.pop('object_list')
        pk = self.kwargs.get('pk')
        for_section = Section.objects.get(id = pk)
        qsmapping = SectionQuestionMapping.objects.filter(for_section = for_section)
        qsmapping_q_id = []
        for i in qsmapping:
            qsmapping_q_id.append(i.for_question.id)
            
        context_object_name = self.context_object_name
        if context_object_name is not None:
            context = {
                context_object_name : queryset,
                'qsmapping' : qsmapping,
                'qsmapping_q_id' : qsmapping_q_id
                }
        return context
    
    def render_to_response(self, context):
        return render(self.request,self.template_name,context)
    
    
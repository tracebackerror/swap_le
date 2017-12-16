from django.shortcuts import render
from django_tables2 import SingleTableView
from django.utils.decorators import method_decorator
from students.models import Student

from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from .models import Assesment, Question
from .tables import AssesmentTable, StudentAssesmentTable
from students.models import Student
from staff.models import Staff

from .models import Assesment
from .forms import AssessmentForm
from django.contrib import messages
from django.shortcuts import *

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



import logging

class ManageAllAssesmentView(SingleTableView, ListView):
    model = Assesment
    context_object_name = 'table'
    paginate_by = 3
    template_name = 'assesments/manage_all_assesment.html'
    table_class = AssesmentTable
    
    #table_data = Staff.active.filter(institute__user__exact=request.user)

    login_decorator = login_required(login_url=reverse_lazy('staff:login'))


    def get_queryset(self):
        #get_associated_staff = Staff.active.filter(staffuser=self.request.user)
        #self.queryset = Student.active.filter(staffuser = get_associated_staff)#active.filter(institute__user__exact=self.request.user)
        self.queryset = Assesment.soft_objects.filter(created_by=self.request.user)
        return super(ManageAllAssesmentView, self).get_queryset()

    @method_decorator(login_decorator)
    def dispatch(self, *args, **kwargs):
        return super(ManageAllAssesmentView, self).dispatch(*args, **kwargs)


    
    def get_context_data(self, **kwargs):
        context = super(ManageAllAssesmentView, self).get_context_data(**kwargs)
       
        return context



class ManageStudentAssesmentView(SingleTableView, ListView):
    model = Assesment
    context_object_name = 'table'
    paginate_by = 3
    template_name = 'assesments/manage_student_assesment.html'
    table_class = StudentAssesmentTable
    http_method_names = ['get', 'post']
    #table_data = Staff.active.filter(institute__user__exact=request.user)

    login_decorator = login_required(login_url=reverse_lazy('student:login'))


    def get_queryset(self):
        #get_associated_staff = Staff.active.filter(staffuser=self.request.user)
        #self.queryset = Student.active.filter(staffuser = get_associated_staff)#active.filter(institute__user__exact=self.request.user)
        student_obj = Student.objects.get(studentuser = self.request.user)
        self.queryset = Assesment.soft_objects.filter(subscriber_users = student_obj)
        return super(ManageStudentAssesmentView, self).get_queryset()

    @method_decorator(login_decorator)
    def dispatch(self, *args, **kwargs):
        return super(ManageStudentAssesmentView, self).dispatch(*args, **kwargs)


  
    
        
    @method_decorator(login_decorator)
    def post(self, *args, **kwargs):
        assesment_initiate_flag = self.request.POST.get('start_assesment_boolean', None)
        if assesment_initiate_flag and eval(assesment_initiate_flag):
            asses_unfiltered = self.request.POST.get('assesment_obj', None)
            page_of_question = int(self.request.POST.get('page', 1))
            
            if asses_unfiltered and eval(asses_unfiltered):
                assesment_to_undertake = Assesment.soft_objects.get(id = eval(asses_unfiltered))
                
                if self.request.user.student in assesment_to_undertake.subscriber_users.all():
                    fetch_all_linked_question = Question.soft_objects.filter(assesment_linked = assesment_to_undertake)
                    paginator = Paginator(fetch_all_linked_question, 3)
                    
                    logging.info("Can Proceed For Assesment")
                    
                    try:
                        page_question_obj = paginator.page(page_of_question)
                    except PageNotAnInteger:
                        page_question_obj = paginator.page(1)
                    except EmptyPage:
                        page_question_obj = paginator.page(paginator.num_pages)
                    
                    # Check whether user has answered any question
                    
                    
                    return render(self.request, 'assesments/exam_start_main_page.html', {
                        'assesment_object': assesment_to_undertake,
                        'all_question_to_answer':page_question_obj,
                        })
                    
        else:
            examid = self.request.POST.get('examid', None)
            assesment_to_undertake = Assesment.soft_objects.get(id = int(examid))
            
            return render(self.request, 'assesments/exam_start_intro_page.html', {
            'assesment_object': assesment_to_undertake,
            })#, content_type='application/xhtml+xml')
            
    
    
    def get_context_data(self, **kwargs):
        context = super(ManageStudentAssesmentView, self).get_context_data(**kwargs)
       
        return context 
    
    

class ProcesStudentAssesmentView(DetailView):
    model = Assesment
    context_object_name = 'table'
    paginate_by = 3
    template_name = 'assesments/manage_student_assesment.html'
    http_method_names = ['get', 'post']
    #table_data = Staff.active.filter(institute__user__exact=request.user)

    login_decorator = login_required(login_url=reverse_lazy('student:login'))


    def get_queryset(self):
        student_obj = Student.objects.get(studentuser = self.request.user)
        self.queryset = Assesment.soft_objects.filter(subscriber_users = student_obj)
        return super(ProcesStudentAssesmentView, self).get_queryset()

    @method_decorator(login_decorator)
    def dispatch(self, *args, **kwargs):
        return super(ProcesStudentAssesmentView, self).dispatch(*args, **kwargs)

    def _process_assesment(self, *args, **kwargs):
        assesment_initiate_flag = self.request.POST.get('start_assesment_boolean', None)
        if assesment_initiate_flag and eval(assesment_initiate_flag):
            asses_unfiltered = self.request.POST.get('assesment_obj', None)
            page_of_question = int(self.request.POST.get('page', 1))
            
            if asses_unfiltered and eval(asses_unfiltered):
                assesment_to_undertake = Assesment.soft_objects.get(id = eval(asses_unfiltered))
                
                if self.request.user.student in assesment_to_undertake.subscriber_users.all():
                    fetch_all_linked_question = Question.soft_objects.filter(assesment_linked = assesment_to_undertake).order_by('pk')

                    paginator = Paginator(fetch_all_linked_question, 1)
                    
                    logging.info("Can Proceed For Assesment")
                    
                    try:
                        page_question_obj = paginator.page(page_of_question)
                    except PageNotAnInteger:
                        page_question_obj = paginator.page(1)
                    except EmptyPage:
                        page_question_obj = paginator.page(paginator.num_pages)
                    
                    # Check whether user has answered any question
                    return render(self.request, 'assesments/exam_start_main_page.html', {
                        'assesment_object': assesment_to_undertake,
                        'all_question_to_answer':page_question_obj,
                        })
                    
        else:
            examid = self.request.POST.get('examid', None)
            assesment_to_undertake = Assesment.soft_objects.get(id = int(examid))
            
            return render(self.request, 'assesments/exam_start_intro_page.html', {
            'assesment_object': assesment_to_undertake,
            })#, content_type='application/xhtml+xml')
            
    
    @method_decorator(login_decorator)
    def get(self, *args, **kwargs):
        self._process_assesment(self, *args, **kwargs)
    
        
    @method_decorator(login_decorator)
    def post(self, *args, **kwargs):
        return self._process_assesment(self, *args, **kwargs)

    
    def get_context_data(self, **kwargs):
        context = super(ProcesStudentAssesmentView, self).get_context_data(**kwargs)
       
        return context 
    
    
    
@login_required(login_url="/staff/login/")
def assessment_delete_by_staff(request, assesmentid):
    information = ''
    
    if hasattr(request.user, 'staff'):
        if request.method == 'GET' and request.user.staff.user_type in ['staff','institution']:
            information = 'Are you sure you want to delete assessmentid {} ?'.format(str(assesmentid))
        elif request.method == 'POST' and request.user.staff.user_type == 'staff':
            staff_obj = Staff.objects.get(staffuser__username=request.user)
            assesment_obj = Assesment.soft_objects.get(id__exact=assesmentid)
            if Assesment.created_by == request.user:
                assesment_obj.delete(request.user)
                assesment_obj.save()
                information = 'Assessment Deleted Successfully. '
            else:
                information = 'You don\'t have authorized permission to delete this record '
                
                
        return render(request, 'assesments/assesment_delete_by_staff.html', {'information': [information]})
    

    
    
@login_required(login_url="/staff/login/")
def assessment_edit_by_staff(request, assesmentid):
    if request.method == 'POST':
        assesment_form = AssessmentForm(instance=Assesment.objects.get(id=assesmentid),
                                 data=request.POST)
        if assesment_form.is_valid():
            assesment_form.save()
            messages.success(request, 'Assessment Updated Successfully')
            #messages.add_message(request, messages.SUCCESS, 'Assessment Updated Successfully')
            return HttpResponseRedirect('/staff/manage/{}/edit/'.format(assesmentid))
    else:
        assesment_form = AssessmentForm(instance=Assesment.objects.get(id=assesmentid)) 
        return render(request, 'assesments/assessment_edit_by_staff.html', {'assessment_form': assesment_form})
    

    
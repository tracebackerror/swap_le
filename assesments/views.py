from django.shortcuts import render, redirect
from django_tables2 import SingleTableView
from django.utils.decorators import method_decorator
from students.models import Student

from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from .models import Assesment, Question
from .tables import AssesmentTable, StudentAssesmentTable, QuestionTable, ResultTable
from .filter import AssesmentFilter
from students.models import Student
from staff.models import Staff

from .models import Assesment, Answer, Result
from .forms import AssessmentForm, AssessmentCreationForm, QuestionForm
from django.contrib import messages
from django.shortcuts import *

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from utility.swaple_constants import all_question_types
from utility import swaple_constants

import logging
from django_tables2 import SingleTableView
from django.views.generic import ListView, DetailView, TemplateView

from .models import Assesment, Question, Answer, Result
from django.views import View
from django.views.generic.detail import SingleObjectMixin

from django_filters.views import   FilterView

from django_tables2.views import SingleTableMixin
from django_tables2 import SingleTableView
from django.views.generic.base import TemplateResponseMixin




class ManageSingleQuestionAddView(TemplateView):
    model = Question
    template_name = 'assesments/manage_add_single_question2.html'
   
    #table_data = Staff.active.filter(institute__user__exact=request.user)
    '''
    def get_success_url(self):
        if 'assesmentid' in self.kwargs:
            self.__assesmentid = self.kwargs['assesmentid']
        else:
            return HttpResponseForbidden()
        return reverse_lazy('staff:assesments:assesment_manage_add_question', kwargs={'assesmentid': self.__assesmentid})
    
    '''
    login_decorator = login_required(login_url=reverse_lazy('staff:login'))
    

    def get_queryset(self):
        self.queryset = super(ManageSingleQuestionAddView, self).get_queryset()
        return self.queryset

    @method_decorator(login_decorator)
    def dispatch(self, *args, **kwargs):
        
        return super(ManageSingleQuestionAddView, self).dispatch(*args, **kwargs)


    @method_decorator(login_decorator)
    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        #return render(request, self.template_name) #, content_type, status, using)("jkj") 
        #messages.get_messages(request).used = True
        
        question_form = QuestionForm() 
        context['question_form'] = question_form
        
        return self.render_to_response(context)
    
        
    @method_decorator(login_decorator)
    def post(self, request, *args, **kwargs):
        if 'assesmentid' in self.kwargs:
            assesment_to_add_question= Assesment.soft_objects.get(id = self.kwargs['assesmentid'])
        
        
        question_form = QuestionForm(data = request.POST or None,
                                     instance= Question(
                                         created_by = request.user,
                                         updated_by = request.user,
                                         assesment_linked = assesment_to_add_question
                                         ))
        redirect_url = request.POST.get('next', None)
        
        
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        
        if question_form and question_form.is_valid():
            question_form.save()
            messages.success(request, 'Question Has Been Added to Assesment.')
            return redirect('staff:assesments:assessment_manage_by_staff', self.kwargs['assesmentid'])
        else:
            context = self.get_context_data()
            context['form_errors'] = question_form.errors
            question_form = QuestionForm(data = request.POST)
            
            
           
            context['question_form'] = question_form
            
        return self.render_to_response(context)
            
    
        
    def get_context_data(self, **kwargs):
        context = super(ManageSingleQuestionAddView, self).get_context_data(**kwargs)
        if 'assesmentid' in self.kwargs:
            context['assesmentid'] = self.kwargs['assesmentid']
        return context 
    
    
class ManageAllAssesmentView(SingleTableMixin, FilterView):
    model = Assesment
    context_object_name = 'table'
    paginate_by = 3
    template_name = 'assesments/manage_all_assesment.html'
    table_class = AssesmentTable
    filterset_class = AssesmentFilter
    
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
        self.queryset = Assesment.soft_objects.filter(subscriber_users = student_obj, privilege='public')
        return super(ManageStudentAssesmentView, self).get_queryset()

    @method_decorator(login_decorator)
    def dispatch(self, *args, **kwargs):
        return super(ManageStudentAssesmentView, self).dispatch(*args, **kwargs)


    
    
        
    @method_decorator(login_decorator)
    def post(self, *args, **kwargs):
        assesment_initiate_flag = self.request.POST.get('start_assesment_boolean', None)
        
        examid = self.request.POST.get('examid', None)
        assesment_to_undertake = Assesment.soft_objects.get(id = int(examid))
        self.request.session['_assesment_to_undertake'] = examid    
        return render(self.request, 'assesments/exam_start_intro_page.html', {
            'assesment_object': assesment_to_undertake,
            })#, content_type='application/xhtml+xml')
            
    
    
    def get_context_data(self, **kwargs):
        context = super(ManageStudentAssesmentView, self).get_context_data(**kwargs)
       
        return context 
    
    
class ManageSingleAsessment(SingleTableView):
    model = Question
    context_object_name = 'table'
    paginate_by = 10
    template_name = 'assesments/manage_single_assesment.html'
    table_class = QuestionTable
    http_method_names = ['get', 'POST']

    login_decorator = login_required(login_url=reverse_lazy('student:login'))
    
    @method_decorator(login_decorator)
    def dispatch(self, *args, **kwargs):
        
        return super(ManageSingleAsessment, self).dispatch(*args, **kwargs)
    
    def get_queryset(self):
        #get_associated_staff = Staff.active.filter(staffuser=self.request.user)
        #self.queryset = Student.active.filter(staffuser = get_associated_staff)#active.filter(institute__user__exact=self.request.user)
        queryset = super(ManageSingleAsessment, self).get_queryset()
        self.assesment_number_to_retrieve = self.kwargs.get('assesmentid', None)
        self.queryset = Question.soft_objects.filter(assesment_linked__exact = self.assesment_number_to_retrieve).order_by('pk')
        return self.queryset
    
    @method_decorator(login_decorator)
    def post(self, *args, **kwargs):
        return self._process_assesment(self, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(ManageSingleAsessment, self).get_context_data(**kwargs)
        self.result_queryset = Result.soft_objects.filter(assesment__exact = self.assesment_number_to_retrieve).order_by('pk')
        context['table_result'] =  ResultTable(self.result_queryset)
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
        get_the_answer_obj = None
        page_question_obj = None
        
        if 'start_assesment_boolean' in self.request.POST.keys():
            assesment_initiate_flag = eval(self.request.POST.get('start_assesment_boolean', None))
        elif '_assesment_initiate_flag' in self.request.session.keys():
            assesment_initiate_flag = self.request.session.get('_assesment_initiate_flag')
             
        if assesment_initiate_flag:
            self.request.session['_assesment_initiate_flag'] = assesment_initiate_flag
            asses_unfiltered = self.request.session.get('_assesment_to_undertake', None)
            page_of_question = int(self.request.POST.get('nextpage', 1))
            
            if asses_unfiltered and eval(asses_unfiltered):
                assesment_to_undertake = Assesment.soft_objects.get(id = eval(asses_unfiltered))
                
                if self.request.user.student in assesment_to_undertake.subscriber_users.all():
                    ''' Getting Next Question'''
                    fetch_all_linked_question = Question.soft_objects.filter(assesment_linked = assesment_to_undertake).order_by('pk')
                    total_question_on_single_page = 1
                    
                    paginator = Paginator(fetch_all_linked_question, total_question_on_single_page)
                    
                    logging.info("Can Proceed For Assesment")
                    
                    try:
                        page_question_obj = paginator.page(page_of_question)
                    except PageNotAnInteger:
                        page_question_obj = paginator.page(1)
                    except EmptyPage:
                        page_question_obj = paginator.page(paginator.num_pages)
                        
                    
                    ''' Log the Answer in Database '''
                    question_type = self.request.POST.get('question_type', None)
                    
                    result_of_assesment = Result.soft_objects.filter(assesment = assesment_to_undertake, registered_user = self.request.user.student
                    )
                    
                    if len(result_of_assesment)  == 0:
                        self.create_result_instance = Result()
                        self.create_result_instance.assesment = assesment_to_undertake
                        self.create_result_instance.registered_user = self.request.user.student
                        self.create_result_instance.created_by = self.request.user
                        self.create_result_instance.updated_by = self.request.user
                        self.create_result_instance.save()
                    else:
                        self.create_result_instance = result_of_assesment[0]
                        
                    if question_type and question_type in all_question_types:
                        pk_of_question = self.request.POST.get('question_id')
                        question_obj = Question.soft_objects.filter(assesment_linked = assesment_to_undertake, pk = pk_of_question)
                        get_the_answer_obj = Answer.soft_objects.filter(for_result = self.create_result_instance, for_question = question_obj)
                        
                        if len(get_the_answer_obj) == 0:
                            get_the_answer_obj = Answer()
                            get_the_answer_obj.created_by = self.request.user
                            get_the_answer_obj.updated_by = self.request.user
                            get_the_answer_obj.for_result = self.create_result_instance
                            get_the_answer_obj.for_question = question_obj[0]
                            #get_the_answer_obj.save()
                        else:
                            get_the_answer_obj = get_the_answer_obj[0]
                            
                        
                        if question_type == swaple_constants.SCQ or question_type == swaple_constants.MCQ:
                            selected_answer = self.request.POST.getlist('answer')
                            get_the_answer_obj.opted_choice = selected_answer
                            # Here we need to add code for checking and setting the marks from question_obj
                            get_the_answer_obj.alloted_marks = 0
                            get_the_answer_obj.save()
                        elif question_type == swaple_constants.SQA:
                            written_answer= self.request.POST.get('answer')
                            get_the_answer_obj.opted_choice = ''
                            get_the_answer_obj.written_answer = written_answer
                            # Here we need to add code for checking and setting the marks from question_obj
                            get_the_answer_obj.alloted_marks = 0
                            get_the_answer_obj.save()
                        
                    else:
                        pass
                    
                        
                    get_the_current_answer_obj = Answer.soft_objects.filter(for_result = self.create_result_instance, for_question = page_question_obj[0])
                        
                    if len(get_the_current_answer_obj) == 0:
                            get_the_current_answer_obj = Answer()
                            get_the_current_answer_obj.created_by = self.request.user
                            get_the_current_answer_obj.updated_by = self.request.user
                            get_the_current_answer_obj.for_result = self.create_result_instance
                            
                            get_the_current_answer_obj.for_question = page_question_obj[0]
                            get_the_current_answer_obj.alloted_marks = 0
                            #get_the_answer_obj.save()
                    else:
                            get_the_current_answer_obj = get_the_current_answer_obj[0]
                            
                    get_the_current_answer_obj.save()
                        
                    # Check whether user has answered any question
                    return render(self.request, 'assesments/exam_start_main_page.html', {
                        'assesment_object': assesment_to_undertake,
                        'all_question_to_answer':page_question_obj,
                        'get_the_answer_obj':get_the_current_answer_obj,
                        })
        else:
            '''
            examid = self.request.POST.get('examid', None)
            assesment_to_undertake = Assesment.soft_objects.get(id = int(examid))
            
            return render(self.request, 'assesments/exam_start_intro_page.html', {
            'assesment_object': assesment_to_undertake,
            })#, content_type='application/xhtml+xml')
            '''
            pass
    
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
            if assesment_obj.created_by == request.user:
                assesment_obj.delete(request.user)
                information = 'Assessment Deleted Successfully. '
            else:
                information = 'You don\'t have authorized permission to delete this record '
                
                
        return render(request, 'assesments/assesment_delete_by_staff.html', {'information': [information]})
    

    
    
@login_required(login_url="/staff/login/")
def assessment_edit_by_staff(request, assesmentid):
    messages.get_messages(request).used = True
    if request.method == 'POST':
        assesment_form = AssessmentForm(instance=Assesment.objects.get(id=assesmentid),request=request,
                                 data=request.POST)
        if assesment_form.is_valid():
            assesment_form.save()
            #messages.success(request, 'Assessment Updated Successfully')
            messages.add_message(request, messages.SUCCESS, 'Assessment Updated Successfully')
            
    else:
        assesment_form = AssessmentForm(request=request,instance=Assesment.objects.get(id=assesmentid)) 
        
    return render(request, 'assesments/assessment_edit_by_staff.html', {'assessment_form': assesment_form})
    



@login_required(login_url="/staff/login/")
def assessment_create_by_staff(request):
    if request.method == 'POST':
        assesment_creation_form = AssessmentCreationForm(request.POST, request=request)
        if assesment_creation_form.is_valid():
            
            saved_new_assesment = assesment_creation_form.save(commit=False)
            saved_new_assesment.created_by = request.user
            saved_new_assesment.updated_by = request.user
            saved_new_assesment.save()
            assesment_creation_form.save_m2m()
            #messages.success(request, 'Assessment Updated Successfully')
            messages.add_message(request, messages.SUCCESS, 'Assessment Created Successfully')
            
    else:
        assesment_creation_form = AssessmentCreationForm(request= request)
        
    return render(request, 'assesments/assessment_create_by_staff.html', {'assessment_c_form': assesment_creation_form})


@login_required(login_url="/staff/login/")
def assessment_question_delete(request,questionid):
    information = ''
    if request.method == 'GET':
        information = 'Are you sure you want to delete question set which id is  {} ?'.format(str(questionid))
        
    elif request.method == 'POST':
        question_obj = Question.objects.get(pk=questionid)
        if question_obj.created_by == request.user:
            question_obj.delete(request.user)
            information = 'Question Deleted Successfully. '
        else:
            information = 'You don\'t have authorized permission to delete this Question. '
   
    return render(request, 'assesments/assesment_question_delete.html', {'information': [information]})
    

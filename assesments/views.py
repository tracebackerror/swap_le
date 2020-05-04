from django.shortcuts import render, redirect
from django_tables2 import SingleTableView
from django.utils.decorators import method_decorator
from django.utils import timezone
from students.models import Student
import base64, os
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.timezone import make_aware
from .models import Assesment, Question
from .tables import AssesmentTable, StudentAssesmentTable, QuestionTable, ResultTable
from .filter import AssesmentFilter
from students.models import Student
from staff.models import Staff
import pytz
from .models import Assesment, Answer, Result
from .forms import AssessmentForm, AssessmentCreationForm, QuestionForm, ReviewSqaAnswerForm, ReviewSqaFormSet, ReviewSqaFormSetHelper
from django.contrib import messages
from django.shortcuts import *

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from utility.swaple_constants import all_question_types
from utility import swaple_constants

import logging
from django_tables2 import SingleTableView
from django_tables2.export.export import TableExport
from django_tables2 import RequestConfig
from django.views.generic import ListView, DetailView, TemplateView, UpdateView

from .models import Assesment, Question, Answer, Result
from django.views import View
from django.views.generic.detail import SingleObjectMixin

from django_filters.views import   FilterView

from django_tables2.views import SingleTableMixin
from django_tables2 import SingleTableView
from django_tables2.export.views import ExportMixin


from django.views.generic.base import TemplateResponseMixin, RedirectView

from django.db.models import Sum, Q

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from datetime import datetime

from section.tables import ManageSectionTable
from section.models import Section,SectionQuestionMapping
from django.db.models import Count
from django.db.models import CharField, Value, F, IntegerField
from base64 import b64encode
from django.template.defaulttags import register
import pandas as pd

from dal import autocomplete
from taggit.models import Tag

import uuid
from django.contrib.auth.models import User
class ReviewAllSqaView(TemplateView):
    model = Answer
    template_name = 'assesments/review_all_sqa.html'
    login_decorator = login_required(login_url=reverse_lazy('staff:login'))
    

    def get_queryset(self):
        self.queryset = super(ReviewAllSqaView, self).get_queryset()
        return self.queryset

    @method_decorator(login_decorator)
    def dispatch(self, *args, **kwargs):
        return super(ReviewAllSqaView, self).dispatch(*args, **kwargs)


    @method_decorator(login_decorator)
    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        #return render(request, self.template_name) #, content_type, status, using)("jkj") 
        #messages.get_messages(request).used = True
        
        
        associated_answer_obj = Answer.objects.filter(for_result__assesment__id = self.kwargs['assesmentid'], for_question__question_type = 'sqa')
        answer_formset = ReviewSqaFormSet(queryset=associated_answer_obj)
        answer_formset_helper = ReviewSqaFormSetHelper()
        
        '''
        answer_forms = []
        for i in associated_answer_obj:
            answer_forms.append(ReviewSqaAnswerForm(instance = i) )
        
        
        context['answer_forms'] = answer_forms
        '''
        context['answer_formset'] = answer_formset
        context['answer__required_review_count'] = len(associated_answer_obj)
        context['answer_formset_helper'] = answer_formset_helper
        
        return self.render_to_response(context)
    
        
    @method_decorator(login_decorator)
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        
        answer_formset = ReviewSqaFormSet(request.POST or None)
        
        answer_formset.save()
        
        associated_answer_obj = Answer.objects.filter(for_result__assesment__id = self.kwargs['assesmentid'], for_question__question_type = 'sqa')
        answer_formset = ReviewSqaFormSet(initial = request.POST, queryset=associated_answer_obj)
        answer_formset_helper = ReviewSqaFormSetHelper()
        
        
        assesment_to_submit = self.kwargs['assesmentid']
        fetch_appropriate_result = Result.objects.filter(assesment__id = assesment_to_submit)
        
        if fetch_appropriate_result.exists():
            get_assesment_obj_to_update = fetch_appropriate_result[0]
            get_assesment_obj_to_update.assesment_submitted = True
            get_assesment_obj_to_update.total_question =  get_assesment_obj_to_update.assesment.question_set.count()
            get_assesment_obj_to_update.total_attempted = get_assesment_obj_to_update.answer_set.all().count()
            
            sum_of_marks = get_assesment_obj_to_update.assesment.question_set.aggregate(sum_of_marks = Sum('max_marks'))
            get_assesment_obj_to_update.total_marks  = sum_of_marks['sum_of_marks']
            
            obtained_marks_calculate = get_assesment_obj_to_update.answer_set.aggregate(answer_obtained_marks = Sum('alloted_marks'))
            get_assesment_obj_to_update.obtained_marks = obtained_marks_calculate.get('answer_obtained_marks')
            get_assesment_obj_to_update.result_passed = obtained_marks_calculate.get('answer_obtained_marks') >= get_assesment_obj_to_update.assesment.passing_marks  
            get_assesment_obj_to_update.save()
        messages.success(request, 'Result Has Been Updated')
            
        
        
        return redirect(reverse_lazy("staff:assesments:assessment_manage_by_staff", kwargs={'assesmentid': self.kwargs['assesmentid']}))

    def get_context_data(self, **kwargs):
        context = super(ReviewAllSqaView, self).get_context_data(**kwargs)
        if 'assesmentid' in self.kwargs:
            context['assesmentid'] = self.kwargs['assesmentid']
        return context 
    
    
    
class GenerateOpenAssesmentResultView(TemplateView):
    http_method_names = [ 'post',]
    template_name = 'assesments/review_all_sqa.html'
    def get_queryset(self):
        self.queryset = super(GenerateOpenAssesmentResultView, self).get_queryset()
        return self.queryset

    def dispatch(self, *args, **kwargs):
        return super(GenerateOpenAssesmentResultView, self).dispatch(*args, **kwargs)

            
    def post(self, request, *args, **kwargs):
        '''
        1. Before Submission Check Whether resultid is in loggedinuser == usersubmission
        2. Only once submission allowed -- Multiple Allowed
        3. Not allow other user exams to be submitted
        4. Calculate Result
        5. And pop out the assesement from student view
        
'''
        assesment_to_submit = self.request.session.get('assesment_to_undertake')
        result_for_student_user = User.objects.get( username = self.request.session['anonymous_student_id'])
        fetch_appropriate_result = Result.objects.filter(assesment__id = assesment_to_submit, registered_user = result_for_student_user.student)
        
        if fetch_appropriate_result.exists():
            get_assesment_obj_to_update = fetch_appropriate_result[0]
            get_assesment_obj_to_update.assesment_submitted = True
            get_assesment_obj_to_update.total_question =  get_assesment_obj_to_update.assesment.question_set.count()
            get_assesment_obj_to_update.total_attempted = get_assesment_obj_to_update.answer_set.all().count()
            
            sum_of_marks = get_assesment_obj_to_update.assesment.question_set.aggregate(sum_of_marks = Sum('max_marks'))
            get_assesment_obj_to_update.total_marks  = sum_of_marks['sum_of_marks']
            
            obtained_marks_calculate = get_assesment_obj_to_update.answer_set.aggregate(answer_obtained_marks = Sum('alloted_marks'))
            get_assesment_obj_to_update.obtained_marks = obtained_marks_calculate.get('answer_obtained_marks')
            get_assesment_obj_to_update.result_passed = obtained_marks_calculate.get('answer_obtained_marks') >= get_assesment_obj_to_update.assesment.passing_marks  
            get_assesment_obj_to_update.save()
            messages.success(request, 'Assesment Has Been Completed')
            
            return redirect(reverse('staff:assesments:assessment_open_result_by_staff', kwargs= {'slug': get_assesment_obj_to_update.assesment.slug, 'pk': get_assesment_obj_to_update.pk}))
            
        else:
            raise NotImplementedError("Implementation Is Stale")
    
    def get_context_data(self, **kwargs):
        context = super(GenerateOpenAssesmentResultView, self).get_context_data(**kwargs)
        if 'assesmentid' in self.kwargs:
            context['assesmentid'] = self.kwargs['assesmentid']
        if 'slug' in self.kwargs:
            context['assesment_slug'] = self.kwargs['slug']
        return context 
        
class GenerateAssesmentResultView(TemplateView):
    http_method_names = [ 'post',]
    template_name = 'assesments/review_all_sqa.html'
    login_decorator = login_required(login_url=reverse_lazy('student:login'))
    

    def get_queryset(self):
        self.queryset = super(GenerateAssesmentResultView, self).get_queryset()
        return self.queryset

    @method_decorator(login_decorator)
    def dispatch(self, *args, **kwargs):
        return super(GenerateAssesmentResultView, self).dispatch(*args, **kwargs)

            
    @method_decorator(login_decorator)
    def post(self, request, *args, **kwargs):
        '''
        1. Before Submission Check Whether resultid is in loggedinuser == usersubmission
        2. Only once submission allowed
        3. Not allow other user exams to be submitted
        4. Calculate Result
        5. And pop out the assesement from student view
        
        
        '''
        assesment_to_submit = self.request.session.get('assesment_to_undertake')
        fetch_appropriate_result = Result.objects.filter(assesment__id = assesment_to_submit, registered_user = self.request.user.student)
        
        if fetch_appropriate_result.exists():
            get_assesment_obj_to_update = fetch_appropriate_result[0]
            get_assesment_obj_to_update.assesment_submitted = True
            get_assesment_obj_to_update.total_question =  get_assesment_obj_to_update.assesment.question_set.count()
            get_assesment_obj_to_update.total_attempted = get_assesment_obj_to_update.answer_set.all().count()
            
            sum_of_marks = get_assesment_obj_to_update.assesment.question_set.aggregate(sum_of_marks = Sum('max_marks'))
            get_assesment_obj_to_update.total_marks  = sum_of_marks['sum_of_marks']
            
            obtained_marks_calculate = get_assesment_obj_to_update.answer_set.aggregate(answer_obtained_marks = Sum('alloted_marks'))
            get_assesment_obj_to_update.obtained_marks = obtained_marks_calculate.get('answer_obtained_marks')
            get_assesment_obj_to_update.result_passed = obtained_marks_calculate.get('answer_obtained_marks') >= get_assesment_obj_to_update.assesment.passing_marks  
            get_assesment_obj_to_update.save()
            messages.success(request, 'Assesment Has Been Completed')
            
            return redirect('student:dashboard')
        else:
            raise NotImplementedError("Implementation Is Stale")
        
        
       
        
    def get_context_data(self, **kwargs):
        context = super(GenerateAssesmentResultView, self).get_context_data(**kwargs)
        if 'assesmentid' in self.kwargs:
            context['assesmentid'] = self.kwargs['assesmentid']
        return context 
    
    
class ManageSingleQuestionUpdateView(LoginRequiredMixin, UpdateView):    
    model = Question
    template_name = 'assesments/manage_add_single_question2.html'
    form_class = QuestionForm
    pk_url_kwarg = 'questionid' 
    
     
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
            assesment_to_add_question= Assesment.objects.get(id = self.kwargs['assesmentid'])
        
        
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
            #import pdb; pdb.set_trace();
            if request.FILES:
                file_extension = request.FILES['question_image'].content_type
                
                encoded_string = base64.b64encode(request.FILES['question_image'].read())
                question_image = 'data:%s;base64,%s' % (file_extension, encoded_string.decode("utf-8"))
            else:
                question_image = None
            
            question_obj=question_form.save()
            question_obj.question_image = question_image
            question_obj.save()
            
            # Processing Existing Result Set to Update the Details
            fetch_appropriate_result = Result.objects.filter(assesment__id = int(self.kwargs['assesmentid']))
        
            if fetch_appropriate_result.exists():
                for each_assesment_result in fetch_appropriate_result:
                    get_assesment_obj_to_update = each_assesment_result
                    
                    get_assesment_obj_to_update.total_question =  get_assesment_obj_to_update.assesment.question_set.count()
                    get_assesment_obj_to_update.total_attempted = get_assesment_obj_to_update.answer_set.all().count()
                    
                    sum_of_marks = get_assesment_obj_to_update.assesment.question_set.aggregate(sum_of_marks = Sum('max_marks'))
                    get_assesment_obj_to_update.total_marks  = sum_of_marks['sum_of_marks']
                    
                    check_if_sqa_is_reviewed = get_assesment_obj_to_update.answer_set.aggregate(answer_obtained_marks = Sum('alloted_marks'))
                    if check_if_sqa_is_reviewed.get('answer_obtained_marks'):
                        obtained_marks_calculate = get_assesment_obj_to_update.answer_set.aggregate(answer_obtained_marks = Sum('alloted_marks'))
                        get_assesment_obj_to_update.obtained_marks = obtained_marks_calculate.get('answer_obtained_marks')
                        get_assesment_obj_to_update.result_passed = obtained_marks_calculate.get('answer_obtained_marks') >= get_assesment_obj_to_update.assesment.passing_marks  
                    get_assesment_obj_to_update.save()
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
    
    
class ManageAllAssesmentView(PermissionRequiredMixin, ExportMixin, SingleTableMixin, FilterView ):
    export_name =  "Assessment Dataset"
    model = Assesment
    context_object_name = 'table'
    paginate_by = 20
    template_name = 'assesments/manage_all_assesment.html'
    table_class = AssesmentTable
    filterset_class = AssesmentFilter
    permission_required = 'staff.is_staff'
    
    #table_data = Staff.active.filter(institute__user__exact=request.user)

    login_decorator = login_required(login_url=reverse_lazy('staff:login'))


    def get_queryset(self):
        #get_associated_staff = Staff.active.filter(staffuser=self.request.user)
        #self.queryset = Student.active.filter(staffuser = get_associated_staff)#active.filter(institute__user__exact=self.request.user)
        self.queryset = Assesment.objects.filter(created_by=self.request.user)
        
        return super(ManageAllAssesmentView, self).get_queryset()

    @method_decorator(login_decorator)
    def dispatch(self, *args, **kwargs):
        return super(ManageAllAssesmentView, self).dispatch(*args, **kwargs)


    
    def get_context_data(self, **kwargs):
        context = super(ManageAllAssesmentView, self).get_context_data(**kwargs)
        '''
        RequestConfig(self.request).configure(self.table_class)

        export_format = request.GET.get("_export", None)
        if TableExport.is_valid_format(export_format):
            exporter = TableExport(export_format, self.table_class)
            return exporter.response("table.{}".format(export_format))'''
        return context

class AssessmentOpenResultByStaff( DetailView):
    model = Result
    template_name = 'assesments/open_display_single_result.html'
    
    def render_to_response(self, context, **response_kwargs):
        #data to required in graph result view =========================================================================
        slug = self.kwargs.get('slug')
        pk = self.kwargs.get('pk')
        result_obj = Result.objects.get(id = pk)
        curr_assessment = result_obj.assesment
        #section_obj = SectionQuestionMapping.objects.filter(for_section__linked_assessment = curr_assessment).values('for_section__name').annotate(count_question = Count('for_question'))
        ans_obj = Answer.objects.filter(for_result = result_obj)
        data = [];
        #print(ans_obj)
        attempted , corrected,total = 0,0,0
        q1 = ans_obj.values('alloted_marks', question_id = F('for_question__id') )
        q2 = Section.objects.filter(linked_assessment = curr_assessment).values('name', question_id = F('for_question__id')).exclude(question_id__isnull=True)

        p1 = pd.DataFrame(q1)
        p2 = pd.DataFrame(q2)
        if not (p1.empty or p2.empty):
            p1.question_id.astype('int') 
            p2.question_id.astype('int') 
            joined_marks_question_and_section = p1.merge(p2)
            sum_df = joined_marks_question_and_section.groupby('name')['alloted_marks'].agg('sum')
        
        
            context['section_name'] = sum_df.to_dict()
        else:
            context['section_name'] = dict()
        return self.response_class(
            request = self.request,
            template = self.get_template_names(),
            context = context,
            **response_kwargs
        )
        
class AssessmentResultByStaff(LoginRequiredMixin, DetailView):
    
    model = Result
    template_name = 'assesments/display_single_result.html'
    login_decorator = login_required(login_url=reverse_lazy('staff:login'))
    
    @method_decorator(login_decorator)
    def dispatch(self, *args, **kwargs):
        return super(AssessmentResultByStaff, self).dispatch(*args, **kwargs)
    
    def render_to_response(self, context, **response_kwargs):
        #data to required in graph result view =========================================================================
        pk = self.kwargs.get('pk')
        result_obj = Result.objects.get(id = pk)
        curr_assessment = result_obj.assesment
        #section_obj = SectionQuestionMapping.objects.filter(for_section__linked_assessment = curr_assessment).values('for_section__name').annotate(count_question = Count('for_question'))
        ans_obj = Answer.objects.filter(for_result = result_obj)
        data = [];
        #print(ans_obj)
        attempted , corrected,total = 0,0,0
        q1 = ans_obj.values('alloted_marks', question_id = F('for_question__id') )
        q2 = Section.objects.filter(linked_assessment = curr_assessment).values('name', question_id = F('for_question__id')).exclude(question_id__isnull=True)

        p1 = pd.DataFrame(q1)
        p2 = pd.DataFrame(q2)
        if not (p1.empty or p2.empty):
            p1.question_id.astype('int') 
            p2.question_id.astype('int') 
            joined_marks_question_and_section = p1.merge(p2)
            sum_df = joined_marks_question_and_section.groupby('name')['alloted_marks'].agg('sum')
        
        
            context['section_name'] = sum_df.to_dict()
        else:
            context['section_name'] = dict()
        return self.response_class(
            request = self.request,
            template = self.get_template_names(),
            context = context,
            **response_kwargs
        )
    
class OpenIntroStudentAssesmentView( DetailView):
    model = Assesment
    
    slug_field = 'slug'
    template_name = 'assesments/open_exam_start_intro_page.html'
    context_object_name = "assesment_object"
    
    
    def get_context_data(self, **kwargs):
        context = super(OpenIntroStudentAssesmentView, self).get_context_data(**kwargs)
        context['meta'] = self.get_object().as_meta(self.request)
        return context
        
class StartIntroStudentAssesmentView( DetailView):
    model = Assesment
    
    slug_field = 'slug'
    template_name = 'assesments/exam_start_intro_page.html'
    context_object_name = "assesment_object"
    
    login_decorator = login_required(login_url=reverse_lazy('student:login'))
    @method_decorator(login_decorator)
    def dispatch(self, *args, **kwargs):
        return super(StartIntroStudentAssesmentView, self).dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(StartIntroStudentAssesmentView, self).get_context_data(**kwargs)
        context['meta'] = self.get_object().as_meta(self.request)
        return context
    '''
    pk_url_kwarg = 'assesmentid'
    paginate_by = 1
    
    http_method_names = ['get', 'post']
    
    
       
     '''
class ManageOpenAssesmentView(SingleTableView, ListView):
    model = Assesment
    context_object_name = 'table'
    paginate_by = 20
    template_name = 'assesments/open_view_assesment.html'
    table_class = StudentAssesmentTable
    http_method_names = ['get', 'post']
    
    def get_queryset(self):
        
        #student_obj = Student.objects.get(studentuser = self.request.user)
        
        #all_user_linked_assesment = Assesment.objects.filter(subscriber_users = student_obj, privilege='public')
        all_user_linked_assesment = Assesment.objects.filter( privilege='open')
        all_user_linked_assesment_filter_exam_date = all_user_linked_assesment.filter(exam_start_date_time__lte= timezone.datetime.now(), expired_on__gte=  timezone.datetime.now())
        self.queryset = all_user_linked_assesment_filter_exam_date
    
        return super(ManageOpenAssesmentView, self).get_queryset()

    def dispatch(self, *args, **kwargs):
        return super(ManageOpenAssesmentView, self).dispatch(*args, **kwargs)
    
    def post(self, *args, **kwargs):
        assesment_initiate_flag = self.request.POST.get('start_assesment_boolean', None)
        examid = self.request.POST.get('examid', None)
        assesment_to_undertake = Assesment.objects.get(id = int(examid))
        #self.request.context['meta'] = assesment_to_undertake.as_meta(self.request)
        self.request.session['assesment_to_undertake'] = examid    
        return redirect(reverse_lazy("staff:assesments:student_assesment_intro", kwargs={'assesmentid': examid}))
     
    def get_context_data(self, **kwargs):
        context = super(ManageOpenAssesmentView, self).get_context_data(**kwargs)
        examid = self.request.POST.get('examid', None)
        
        return context     
    
class ManageStudentAssesmentView(SingleTableView, ListView):
    model = Assesment
    context_object_name = 'table'
    paginate_by = 20
    template_name = 'assesments/manage_student_assesment.html'
    table_class = StudentAssesmentTable
    http_method_names = ['get', 'post']
    #table_data = Staff.active.filter(institute__user__exact=request.user)

    login_decorator = login_required(login_url=reverse_lazy('student:login'))


    def get_queryset(self):
        #get_associated_staff = Staff.active.filter(staffuser=self.request.user)
        #self.queryset = Student.active.filter(staffuser = get_associated_staff)#active.filter(institute__user__exact=self.request.user)
        student_obj = Student.objects.get(studentuser = self.request.user)
        
        #self.queryset = Assesment.objects.filter(subscriber_users = student_obj, privilege='public').filter(Q(result__assesment_submitted=False) |  Q(result__isnull=True))
        all_user_linked_assesment = Assesment.objects.filter(subscriber_users = student_obj, privilege='public')
        #all_user_linked_assesment_filter_exam_date = all_user_linked_assesment.filter(exam_start_date_time__lte= timezone.localtime(timezone.now()), expired_on__gte= timezone.localtime(timezone.now()))
        all_user_linked_assesment_filter_exam_date = all_user_linked_assesment.filter(exam_start_date_time__lte= timezone.datetime.now(), expired_on__gte=  timezone.datetime.now())
        
        
        
        if all_user_linked_assesment_filter_exam_date.exists():
            all_user_linked_result = Result.objects.filter(registered_user=student_obj).filter(assesment_submitted=True)
            if all_user_linked_result.exists():
                self.queryset = all_user_linked_assesment_filter_exam_date.exclude(result__in = all_user_linked_result )
            else:
                self.queryset = all_user_linked_assesment_filter_exam_date
        else:
            self.queryset = all_user_linked_assesment_filter_exam_date
    
        return super(ManageStudentAssesmentView, self).get_queryset()

    @method_decorator(login_decorator)
    def dispatch(self, *args, **kwargs):
        return super(ManageStudentAssesmentView, self).dispatch(*args, **kwargs)


    
    
        
    @method_decorator(login_decorator)
    def post(self, *args, **kwargs):
        assesment_initiate_flag = self.request.POST.get('start_assesment_boolean', None)
        examid = self.request.POST.get('examid', None)
        assesment_to_undertake = Assesment.objects.get(id = int(examid))
        #self.request.context['meta'] = assesment_to_undertake.as_meta(self.request)
        self.request.session['assesment_to_undertake'] = examid    
        return redirect(reverse_lazy("staff:assesments:student_assesment_intro", kwargs={'assesmentid': examid}))
            
    
    
    def get_context_data(self, **kwargs):
        context = super(ManageStudentAssesmentView, self).get_context_data(**kwargs)
        examid = self.request.POST.get('examid', None)
        
        return context 
    
    
class ManageSingleAsessment(ExportMixin, SingleTableView):
    export_name =  "Result"
    model = Question
    context_object_name = 'table'
    paginate_by = 20
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
        self.queryset = Question.objects.filter(assesment_linked__exact = self.assesment_number_to_retrieve).order_by('pk')
        return self.queryset
    
    @method_decorator(login_decorator)
    def post(self, *args, **kwargs):
        return self._process_assesment(self, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(ManageSingleAsessment, self).get_context_data(**kwargs)
        
        self.result_queryset = Result.objects.filter(assesment__exact = self.assesment_number_to_retrieve).order_by('pk')
        
        
        result_table =  ResultTable(self.result_queryset, assesmentid=self.kwargs['assesmentid'])
        context['assesment'] = Assesment.objects.get(id = self.kwargs['assesmentid'])
        if self.request.user_agent.is_mobile:
            result_table.exclude += ('exam_taken_date_time', 'total_question', 'total_attempted', 'publish_result', 'assesment_submitted')
            context['table_result']  = result_table
            
        else:
            context['table_result'] = result_table
        self.section_queryset = Section.objects.filter(linked_assessment__id = self.assesment_number_to_retrieve).order_by('pk')
        table_section = ManageSectionTable(self.section_queryset)
        #table_section.paginate(page=self.request.GET.get('page', 1), per_page=1)
        context['table_section'] =  table_section
        
        #Stduent Assessment Progress Bar Data
        total_subscribes_student = Assesment.objects.filter(id = self.kwargs['assesmentid']).aggregate(total_user = Count('subscriber_users'))
        attend_exam_student = Result.objects.filter(assesment__id = self.kwargs['assesmentid'] , assesment_submitted = True).count()
        
        percentage_of_attend_exam = (attend_exam_student / total_subscribes_student['total_user']) * 100
        context['percentage_student'] = round(percentage_of_attend_exam,2)
        context['total_subscribes_student'] = total_subscribes_student['total_user']
        context['attend_exam_student'] = attend_exam_student
        
        #Publish All Results
        result_obj = Result.objects.filter(assesment__id = self.kwargs['assesmentid'])
        flag = True
        count_publish_result = Result.objects.filter(assesment__id = self.kwargs['assesmentid'], publish_result = True).aggregate(count = Count('publish_result'))
        if count_publish_result['count'] == result_obj.count():
            flag = False
        context['flag'] = flag
        
        return context
    
class ProcessOpenAssesmentView(DetailView):
    model = Assesment
    context_object_name = "assesment_object"
    template_name = 'assesments/open_exam_start_main_page.html'
    http_method_names = ['get', 'post']
    
    def _process_assesment(self, *args, **kwargs):
        get_the_answer_obj = None
        page_question_obj = None
        
        if 'start_assesment_boolean' in self.request.POST.keys():
            assesment_initiate_flag = eval(self.request.POST.get('start_assesment_boolean', None))
            time_obj= timezone.now()
            self.request.session['exam_start_time'] = time_obj.strftime("%d/%m/%Y %H:%M")
            self.request.session['exam_start_time_year'] = time_obj.year
            self.request.session['exam_start_time_month'] = time_obj.month
            self.request.session['exam_start_time_day'] = time_obj.day
            self.request.session['exam_start_time_hour'] = time_obj.hour
            self.request.session['exam_start_time_minute'] = time_obj.minute
            user_name = uuid.uuid4().hex[:30]
            user_obj = User.objects.create_user(username=user_name,
                             email='anonymoususer@beatles.com',
                             password='Test@19487d')
            
            student_obj = Student()

            student_obj.studentuser = user_obj
            
            student_obj.save()
            user_obj.save()
            self.request.session['anonymous_student_id'] = user_name
            
        elif '_assesment_initiate_flag' in self.request.session.keys():
            assesment_initiate_flag = self.request.session.get('_assesment_initiate_flag')
             
        if assesment_initiate_flag:
            
            if self.request.POST.get('assesment_obj', None) :
                self.request.session['assesment_to_undertake'] = self.request.POST['assesment_obj']
                
            self.request.session['_assesment_initiate_flag'] = assesment_initiate_flag
            asses_unfiltered = self.request.session.get('assesment_to_undertake', None)
            page_of_question = int(self.request.POST.get('nextpage', 1))
            
            if asses_unfiltered and eval(asses_unfiltered):
                assesment_to_undertake = Assesment.objects.get(id = eval(asses_unfiltered))
                
                ''' Getting Next Question'''
                fetch_all_linked_question = Question.objects.filter(assesment_linked = assesment_to_undertake).order_by('pk')
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
                
                result_for_student_user = User.objects.get( username = self.request.session['anonymous_student_id'])
                
                result_of_assesment = Result.objects.filter(assesment = assesment_to_undertake, registered_user = result_for_student_user.student, exam_taken_date_time__year = self.request.session['exam_start_time_year'], exam_taken_date_time__month = self.request.session['exam_start_time_month'], exam_taken_date_time__day = self.request.session['exam_start_time_day'], exam_taken_date_time__hour = self.request.session['exam_start_time_hour'], exam_taken_date_time__minute = self.request.session['exam_start_time_minute'])
                #result_of_assesment.delete()
                if len(result_of_assesment)  == 0:
                    self.create_result_instance = Result()
                    #exam_taken_date_time use for exam time
                    time_obj= timezone.now()
                    self.request.session['exam_start_time'] = time_obj.strftime("%d/%m/%Y %H:%M")
                    self.request.session['exam_start_time_year'] = time_obj.year
                    self.request.session['exam_start_time_month'] = time_obj.month
                    self.request.session['exam_start_time_day'] = time_obj.day
                    self.request.session['exam_start_time_hour'] = time_obj.hour
                    self.request.session['exam_start_time_minute'] = time_obj.minute
                    self.create_result_instance.exam_taken_date_time = time_obj
                    self.create_result_instance.assesment = assesment_to_undertake
                    self.create_result_instance.registered_user = result_for_student_user.student
                    self.create_result_instance.created_by = result_for_student_user
                    self.create_result_instance.updated_by = result_for_student_user
                    self.create_result_instance.save()
                else:
                    self.create_result_instance = result_of_assesment[0]
                
                '''
                if len(result_of_assesment)  == 0:
                    difference =  timezone.now() -  timezone.now() 
                else:
                    difference =  timezone.now() - self.create_result_instance.exam_taken_date_time 
                seconds_in_day = 24 * 60 * 60
                alloted_seconds = (assesment_to_undertake.duration_hours * 60 + assesment_to_undertake.duration_minutes) * 60
                minutes_cumulative_over, seconds_over = divmod(difference.seconds, 60)
                hours_over, minutes_over = divmod(minutes_cumulative_over, 60)
                
                if hours_over >= assesment_to_undertake.duration_hours and minutes_over >= assesment_to_undertake.duration_minutes:
                    # Time Over Exit Assesment
                    self.create_result_instance.assesment_submitted = True
                    self.create_result_instance.total_question =  self.create_result_instance.assesment.question_set.count()
                    self.create_result_instance.total_attempted = self.create_result_instance.answer_set.all().count()
                        
                    sum_of_marks = self.create_result_instance.assesment.question_set.aggregate(sum_of_marks = Sum('max_marks'))
                    self.create_result_instance.total_marks  = sum_of_marks['sum_of_marks']
                        
                    obtained_marks_calculate = self.create_result_instance.answer_set.aggregate(answer_obtained_marks = Sum('alloted_marks'))
                    if obtained_marks_calculate.get('answer_obtained_marks'):
                        self.create_result_instance.obtained_marks = obtained_marks_calculate.get('answer_obtained_marks')
                    
                        self.create_result_instance.result_passed = obtained_marks_calculate.get('answer_obtained_marks') >= self.create_result_instance.assesment.passing_marks  
                    else:
                        self.create_result_instance.obtained_marks = 0
                        self.create_result_instance.result_passed = False
                    self.create_result_instance.save()

                    messages.success(self.request, 'Alloted Time Over: Assesment Test Has Been Submitted')
                    return redirect(reverse('staff:assesments:assessment_open_result_by_staff', kwargs= {'slug': self.create_result_instance.assesment.slug, 'pk': self.create_result_instance.pk}))
                '''    
                
                if question_type and question_type in all_question_types:
                    pk_of_question = self.request.POST.get('question_id')
                    question_obj = Question.objects.filter(assesment_linked = assesment_to_undertake, pk = pk_of_question)
                    get_the_answer_obj = Answer.objects.filter(for_result = self.create_result_instance, for_question__in = question_obj)
                    #import pdb; pdb.set_trace();
                    
                    if len(get_the_answer_obj) == 0:
                        get_the_answer_obj = Answer()
                        get_the_answer_obj.created_by = result_for_student_user
                        get_the_answer_obj.updated_by = result_for_student_user
                        get_the_answer_obj.for_result = self.create_result_instance
                        get_the_answer_obj.for_question = question_obj[0]
                        #get_the_answer_obj.save()
                    else:
                        get_the_answer_obj = get_the_answer_obj[0]
                        
                    
                    if question_type == swaple_constants.SCQ or question_type == swaple_constants.MCQ:
                        selected_answer = self.request.POST.getlist('answer')
                        get_the_answer_obj.opted_choice = selected_answer
                        # Here we need to add code for checking and setting the marks from question_obj
                        option_selected = "-".join(selected_answer)
                        if option_selected == question_obj[0].correct_options:
                            get_the_answer_obj.alloted_marks = question_obj[0].max_marks
                        else:
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
                
                if len(page_question_obj) == 0 :
                    messages.add_message(self.request, messages.SUCCESS,  'Assessment Test Is Not Having Any Single Question To Answer. ')
                    return redirect(reverse_lazy("staff:assesments:manage_open_assesment"))
                get_the_current_answer_obj = Answer.objects.filter(for_result = self.create_result_instance, for_question = page_question_obj[0])
                
                '''
                if len(get_the_current_answer_obj) == 0:
                        get_the_current_answer_obj = Answer()
                        get_the_current_answer_obj.created_by = result_for_student_user
                        get_the_current_answer_obj.updated_by = result_for_student_user
                        get_the_current_answer_obj.for_result = self.create_result_instance
                        
                        get_the_current_answer_obj.for_question = page_question_obj[0]
                        get_the_current_answer_obj.alloted_marks = 0
                        #get_the_answer_obj.save()
                else:
                        get_the_current_answer_obj = get_the_current_answer_obj[0]
                        
                get_the_current_answer_obj.save() 
                # Check whether user has answered any question
                '''
                
                
                #question image display view
                question_image_obj = {}
                for question in fetch_all_linked_question:
                    if(question.question_image):
                        question_image_obj[question.id] = question.question_image
                   
                return render(self.request, self.template_name, {
                    'assesment_object': assesment_to_undertake,
                    'all_question_to_answer':page_question_obj,
                    'get_the_answer_obj':get_the_current_answer_obj,
                    'result_object':self.create_result_instance,
                    'question_image_obj':question_image_obj,
                    
                    })
     
    @register.filter
    def get_item(dictionary, key):
        return dictionary.get(key)

    def get(self, *args, **kwargs):
        
        asses_unfiltered = self.request.session.get('assesment_to_undertake', None)
        page_of_question = int(self.request.GET.get('nextpage', 1))
        
        if asses_unfiltered and eval(asses_unfiltered):
            assesment_to_undertake = Assesment.objects.get(id = eval(asses_unfiltered))
            
            ''' Getting Next Question'''
            fetch_all_linked_question = Question.objects.filter(assesment_linked = assesment_to_undertake).order_by('pk')
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
            question_type = self.request.GET.get('question_type', None)
            
            result_for_student_user = User.objects.get( username = self.request.session['anonymous_student_id'])
            
            result_of_assesment = Result.objects.filter(assesment = assesment_to_undertake, registered_user = result_for_student_user.student)
            
            self.create_result_instance = result_of_assesment.first()
            
        if question_type and question_type in all_question_types:
            pk_of_question = self.request.GET.get('question_id')
            question_obj = Question.objects.filter(assesment_linked = assesment_to_undertake, pk = pk_of_question)
            get_the_answer_obj = Answer.objects.filter(for_result = self.create_result_instance, for_question__in = question_obj)
            #import pdb; pdb.set_trace();
            
            if len(get_the_answer_obj) == 0:
                get_the_answer_obj = Answer()
                get_the_answer_obj.created_by = result_for_student_user
                get_the_answer_obj.updated_by = result_for_student_user
                get_the_answer_obj.for_result = self.create_result_instance
                get_the_answer_obj.for_question = question_obj[0]
                #get_the_answer_obj.save()
            else:
                get_the_answer_obj = get_the_answer_obj[0]
                
            
            if question_type == swaple_constants.SCQ or question_type == swaple_constants.MCQ:
                selected_answer = self.request.GET.getlist('answer')
                get_the_answer_obj.opted_choice = selected_answer
                # Here we need to add code for checking and setting the marks from question_obj
                option_selected = "-".join(selected_answer)
                if option_selected == question_obj[0].correct_options:
                    get_the_answer_obj.alloted_marks = question_obj[0].max_marks
                else:
                    get_the_answer_obj.alloted_marks = 0
                get_the_answer_obj.save()
            elif question_type == swaple_constants.SQA:
                written_answer= self.request.GET.get('answer')
                get_the_answer_obj.opted_choice = ''
                get_the_answer_obj.written_answer = written_answer
                # Here we need to add code for checking and setting the marks from question_obj
                get_the_answer_obj.alloted_marks = 0
                get_the_answer_obj.save()
            
        else:
            pass
        
        if len(page_question_obj) == 0 :
            messages.add_message(self.request, messages.SUCCESS,  'Assessment Test Is Not Having Any Single Question To Answer. ')
            return redirect(reverse_lazy("staff:assesments:manage_open_assesment"))
        get_the_current_answer_obj = Answer.objects.filter(for_result = self.create_result_instance, for_question = page_question_obj[0]).first()
        
        question_image_obj = {}
        for question in fetch_all_linked_question:
            if (question.question_image):
                question_image_obj[question.id] = question.question_image
           
        return render(self.request, self.template_name, {
            'assesment_object': assesment_to_undertake,
            'all_question_to_answer':page_question_obj,
            'get_the_answer_obj':get_the_current_answer_obj,
            'result_object':self.create_result_instance,
            'question_image_obj':question_image_obj,
            
            })        

    def post(self, *args, **kwargs):
        return self._process_assesment(self, *args, **kwargs)

    
    def get_context_data(self, **kwargs):
        context = super(ProcessOpenAssesmentView, self).get_context_data(**kwargs)
        return context
        
class ProcesStudentAssesmentView(DetailView):
    model = Assesment
    context_object_name = "assesment_object"
    paginate_by = 3
    template_name = 'assesments/manage_student_assesment.html'
    http_method_names = ['get', 'post']
    #table_data = Staff.active.filter(institute__user__exact=request.user)

    login_decorator = login_required(login_url=reverse_lazy('student:login'))


    def get_queryset(self):
        student_obj = Student.objects.get(studentuser = self.request.user)
        self.queryset = Assesment.objects.filter(subscriber_users = student_obj)
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
            if self.request.POST.get('assesment_obj', None):
                self.request.session['assesment_to_undertake'] = self.request.POST['assesment_obj']
            self.request.session['_assesment_initiate_flag'] = assesment_initiate_flag
            asses_unfiltered = self.request.session.get('assesment_to_undertake', None)
            page_of_question = int(self.request.POST.get('nextpage', 1))
            
            if asses_unfiltered and eval(asses_unfiltered):
                assesment_to_undertake = Assesment.objects.get(id = eval(asses_unfiltered))
                
                if self.request.user.student in assesment_to_undertake.subscriber_users.all():
                    ''' Getting Next Question'''
                    fetch_all_linked_question = Question.objects.filter(assesment_linked = assesment_to_undertake).order_by('pk')
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
                    
                    result_of_assesment = Result.objects.filter(assesment = assesment_to_undertake, registered_user = self.request.user.student
                    )
                    
                    if len(result_of_assesment)  == 0:
                        self.create_result_instance = Result()
                        #exam_taken_date_time use for exam time
                        
                        self.create_result_instance.exam_taken_date_time = timezone.now()
                        self.create_result_instance.assesment = assesment_to_undertake
                        self.create_result_instance.registered_user = self.request.user.student
                        self.create_result_instance.created_by = self.request.user
                        self.create_result_instance.updated_by = self.request.user
                        self.create_result_instance.save()
                    else:
                        self.create_result_instance = result_of_assesment[0]
                    
                    difference =  timezone.now() - self.create_result_instance.exam_taken_date_time 
                    seconds_in_day = 24 * 60 * 60
                    alloted_seconds = (assesment_to_undertake.duration_hours * 60 + assesment_to_undertake.duration_minutes) * 60
                    minutes_cumulative_over, seconds_over = divmod(difference.seconds, 60)
                    hours_over, minutes_over = divmod(minutes_cumulative_over, 60)
                    
                    if hours_over >= assesment_to_undertake.duration_hours and minutes_over >= assesment_to_undertake.duration_minutes:
                        # Time Over Exit Assesment
                        self.create_result_instance.assesment_submitted = True
                        self.create_result_instance.total_question =  self.create_result_instance.assesment.question_set.count()
                        self.create_result_instance.total_attempted = self.create_result_instance.answer_set.all().count()
                            
                        sum_of_marks = self.create_result_instance.assesment.question_set.aggregate(sum_of_marks = Sum('max_marks'))
                        self.create_result_instance.total_marks  = sum_of_marks['sum_of_marks']
                            
                        obtained_marks_calculate = self.create_result_instance.answer_set.aggregate(answer_obtained_marks = Sum('alloted_marks'))
                        self.create_result_instance.obtained_marks = obtained_marks_calculate.get('answer_obtained_marks')
                        self.create_result_instance.result_passed = obtained_marks_calculate.get('answer_obtained_marks') >= self.create_result_instance.assesment.passing_marks  
                        self.create_result_instance.save()

                        messages.success(self.request, 'Alloted Time Over: Assesment Test Has Been Submitted')
                        return redirect('student:dashboard')
                        
                    
                    if question_type and question_type in all_question_types:
                        pk_of_question = self.request.POST.get('question_id')
                        question_obj = Question.objects.filter(assesment_linked = assesment_to_undertake, pk = pk_of_question)
                        get_the_answer_obj = Answer.objects.filter(for_result = self.create_result_instance, for_question__in = question_obj)
                        
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
                            option_selected = "-".join(selected_answer)
                            if option_selected == question_obj[0].correct_options:
                                get_the_answer_obj.alloted_marks = question_obj[0].max_marks
                            else:
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
                    
                    if len(page_question_obj) == 0 :
                        messages.add_message(self.request, messages.SUCCESS,  'Assessment Test Is Not Having Any Single Question To Answer. ')
                        return redirect(reverse_lazy("staff:assesments:manage_student_assesment"))
                    get_the_current_answer_obj = Answer.objects.filter(for_result = self.create_result_instance, for_question = page_question_obj[0])
                        
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
                    
                    
                    #question image display view
                    question_image_obj = {}
                    for question in fetch_all_linked_question:
                        if(question.question_image):
                            question_image_obj[question.id] = question.question_image
                       
                    return render(self.request, 'assesments/exam_start_main_page.html', {
                        'assesment_object': assesment_to_undertake,
                        'all_question_to_answer':page_question_obj,
                        'get_the_answer_obj':get_the_current_answer_obj,
                        'result_object':self.create_result_instance,
                        'question_image_obj':question_image_obj,
                        
                        })
                    
        else:
            '''
            examid = self.request.POST.get('examid', None)
            assesment_to_undertake = Assesment.objects.get(id = int(examid))
            
            return render(self.request, 'assesments/exam_start_intro_page.html', {
            'assesment_object': assesment_to_undertake,
            })#, content_type='application/xhtml+xml')
            '''
            pass
        
    def get_success_url(self, **kwargs):         
        
        return reverse_lazy('staff:assesments:process_assesment', kwargs = self.kwargs)
    @register.filter
    def get_item(dictionary, key):
        return dictionary.get(key)

    @method_decorator(login_decorator)
    def get(self, *args, **kwargs):
        self._process_assesment(self, *args, **kwargs)
    
        
    @method_decorator(login_decorator)
    def post(self, *args, **kwargs):
        return self._process_assesment(self, *args, **kwargs)

    
    def get_context_data(self, **kwargs):
        context = super(ProcesStudentAssesmentView, self).get_context_data(**kwargs)
        return context 
    
    
class RegenerateResult(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    login_url=reverse_lazy('home:homeview')
    permission_required = 'staff.is_staff'
    
    def get(self, *args, **kwargs):
        self._process_assesment(self, *args, **kwargs)
    
@login_required(login_url="/staff/login/")
def assessment_delete_by_staff(request, assesmentid):
    information = ''
    
    if hasattr(request.user, 'staff'):
        if request.method == 'GET' and request.user.staff.user_type in ['staff','institution']:
            information = 'Are you sure you want to delete assessmentid {} ?'.format(str(assesmentid))
        elif request.method == 'POST' and request.user.staff.user_type == 'staff':
            staff_obj = Staff.objects.get(staffuser__username=request.user)
            assesment_obj = Assesment.objects.get(id__exact=assesmentid)
            if assesment_obj.created_by == request.user:
                assesment_obj.delete()
                
                messages.add_message(request, messages.SUCCESS,  'Assessment Test Deleted Successfully. ')
                return redirect(reverse_lazy("staff:assesments:manage_all_assesment"))
            else:
                information = 'You don\'t have authorized permission to delete this record '
                
                
        return render(request, 'assesments/assesment_delete_by_staff.html', {'information': [information]})
    

def __recalculate_result(assesment_id = None, *args, **kwargs):
    pass
    
    
@login_required(login_url="/staff/login/")
def assessment_edit_by_staff(request, assesmentid):
    messages.get_messages(request).used = True
    date_time_format = "%d/%m/%Y %H:%M"
    if request.method == 'POST':
        '''
        expired_on = datetime.strptime(request.POST['expired_on'], date_time_format)
        exam_start_date_time = datetime.strptime(request.POST['exam_start_date_time'], date_time_format)
        total_exam_duration_val = str(expired_on - exam_start_date_time)
        '''
        asses_obj = Assesment.objects.get(id=assesmentid) 
        
        assesment_form = AssessmentForm( instance=asses_obj, request=request,
                                 data=request.POST)
        
        if assesment_form.is_valid():
            assesment_form.save()
                    
            fetch_appropriate_result = Result.objects.filter(assesment__id = int(assesmentid))
        
            if fetch_appropriate_result.exists():
                for each_assesment_result in fetch_appropriate_result:
                    get_assesment_obj_to_update = each_assesment_result
                    
                    get_assesment_obj_to_update.total_question =  get_assesment_obj_to_update.assesment.question_set.count()
                    get_assesment_obj_to_update.total_attempted = get_assesment_obj_to_update.answer_set.all().count()
                    
                    sum_of_marks = get_assesment_obj_to_update.assesment.question_set.aggregate(sum_of_marks = Sum('max_marks'))
                    get_assesment_obj_to_update.total_marks  = sum_of_marks['sum_of_marks']
                    obtained_marks_calculate = get_assesment_obj_to_update.answer_set.aggregate(answer_obtained_marks = Sum('alloted_marks'))
                    if obtained_marks_calculate.get('answer_obtained_marks'):
                        get_assesment_obj_to_update.obtained_marks = obtained_marks_calculate.get('answer_obtained_marks')
                        get_assesment_obj_to_update.result_passed = obtained_marks_calculate.get('answer_obtained_marks') >= get_assesment_obj_to_update.assesment.passing_marks  
                    else:
                        get_assesment_obj_to_update.obtained_marks = 0
                        get_assesment_obj_to_update.result_passed = False
                    get_assesment_obj_to_update.save()

                
            #messages.success(request, 'Assessment Updated Successfully')
            messages.add_message(request, messages.SUCCESS, 'Assessment Updated Successfully')
            success_url = reverse_lazy("staff:assesments:manage_all_assesment")
            return HttpResponseRedirect(success_url)
 
    else:   
        assesment_form = AssessmentForm(request=request,instance=Assesment.objects.get(id=assesmentid)) 
        
    return render(request, 'assesments/assessment_create_by_staff.html', {'assessment_c_form': assesment_form})
    



class TagAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        qs = Tag.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

@permission_required('staff.is_staff',login_url=reverse_lazy('staff:login'))
@login_required(login_url=reverse_lazy('staff:login'))
def assessment_create_by_staff(request):
    date_time_format = "%d/%m/%Y %H:%M"
    if request.method == 'POST':
        expired_on = make_aware(datetime.strptime(request.POST['expired_on'], date_time_format))
        exam_start_date_time = make_aware(datetime.strptime(request.POST['exam_start_date_time'], date_time_format))
        total_exam_duration = expired_on - exam_start_date_time
        
        assesment_creation_form = AssessmentCreationForm(request.POST, request=request)
        if assesment_creation_form.is_valid():
            
            saved_new_assesment = assesment_creation_form.save(commit=False)
            #saved_new_assesment.total_exam_duration = str(total_exam_duration)#.strftime('%Y-%m-%d/%H:%M:%S')
            saved_new_assesment.created_by = request.user
            saved_new_assesment.updated_by = request.user
            saved_new_assesment.save()
            assesment_creation_form.save_m2m()
            #import pdb;pdb.set_trace();
            #messages.success(request, 'Assessment Updated Successfully')
            messages.add_message(request, messages.SUCCESS, 'Assessment Created Successfully')
            return redirect(reverse_lazy("staff:assesments:assessment_manage_by_staff", kwargs ={ 'assesmentid' : saved_new_assesment.id }))
            
    else:
        assesment_creation_form = AssessmentCreationForm(request= request)
        
    return render(request, 'assesments/assessment_create_by_staff.html', {'assessment_c_form': assesment_creation_form})


@login_required(login_url="/staff/login/")
def assessment_question_delete(request, assesmentid, questionid ):
    information = ''
    if request.method == 'GET':
        information = 'Are you sure you want to delete question set which id is  {} ?'.format(str(questionid))
        
    elif request.method == 'POST':
        question_obj = Question.objects.get(pk=questionid)
        if question_obj.created_by == request.user:
            #question_obj.delete(request.user)
            question_obj.delete()
            
            messages.add_message(request, messages.SUCCESS,  'Question Deleted Successfully. ')
            return redirect(reverse_lazy("staff:assesments:assessment_manage_by_staff", kwargs={'assesmentid': assesmentid}))
            
        else:
            information = 'You don\'t have authorized permission to delete this Question. '
   
    return render(request, 'assesments/assesment_question_delete.html', {'information': [information]})


@login_required(login_url="/staff/login/")
def PublishAllResults(request,assesmentid):
    result_obj = Result.objects.filter(assesment__id = assesmentid)
    flag = "published"
    count_publish_result = Result.objects.filter(assesment__id = assesmentid, publish_result = True).aggregate(count = Count('publish_result'))
    if count_publish_result['count'] == result_obj.count():
        flag = "unpublished"
     
    if (flag == "published"):
        for result in result_obj:
            result.publish_result = True
            result.save()
        msg = "Published All Results Successfully"
    elif (flag == "unpublished"):
        for result in result_obj:
            result.publish_result = False
            result.save()
        msg = "Un-Published All Results Successfully"

    messages.add_message(request, messages.SUCCESS,msg)
    success_url = reverse("staff:assesments:assessment_manage_by_staff", kwargs = {'assesmentid':assesmentid})
    return HttpResponseRedirect(success_url)







    
    
    
    
    

    

from django.shortcuts import render
from django_tables2 import SingleTableView
from django.utils.decorators import method_decorator
from students.models import Student

from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from .models import Assesment
from .tables import AssesmentTable, StudentAssesmentTable
from students.models import Student

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
        examid = self.request.POST.get('examid', None)
        assesment_to_undertake = Assesment.soft_objects.get(id = int(examid))
        
        return render(self.request, 'assesments/exam_start_intro_page.html', {
        'assesment_object': assesment_to_undertake,
        })#, content_type='application/xhtml+xml')
        pass
    
    
    def get_context_data(self, **kwargs):
        context = super(ManageStudentAssesmentView, self).get_context_data(**kwargs)
       
        return context 
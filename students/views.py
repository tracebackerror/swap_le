from django.http.response import HttpResponse
from django.http.response import HttpResponseRedirect

from django.shortcuts import render
from django.shortcuts import redirect

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.timezone import make_aware
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (PasswordResetView,PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView)
from django.contrib.auth.views import PasswordChangeDoneView, PasswordChangeView, LoginView

from django.utils import timezone
from django.utils.decorators import method_decorator

from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

from django.urls import reverse_lazy
from institutions.forms import UserEditForm
from django.views.generic import ListView,View,FormView

from .filters import ViewLibraryAssetFilter
from .models import Student
from .forms import StudentRegistrationForm

from library.models import AssetHistory
from library.models import LibraryAsset
from assesments.models import Assesment
from assesments.models import Result
from staff.models import Staff

from django_filters.views import FilterView
from django.views.generic import TemplateView
#from easy_pdf.views import PDFTemplateView

from django.db.models import Count
from django.db.models import Sum

from functools import wraps

class InstitutionStudentLoginView(LoginView):
    template_name = 'student/login.html'

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        if hasattr(form.get_user(), 'student') and (form.get_user().student.user_type == 'student'):
            
            student_object = Student.objects.get(studentuser = form.get_user())
            
            #auth_login(self.request, student_object)
            #return HttpResponseRedirect(self.get_success_url())
            return super(InstitutionStudentLoginView, self).form_valid(form)
        else:
            invalidInstitution = 'Not an Valid Student Credentials'
            # if '__all__' in form.errors:
            #     form.errors.update({'__all__': form.errors['__all__'] + [invalidInstitution]})
            # else:
            #     form.errors.update({'__all__': [invalidInstitution]})
            form.add_error(None, invalidInstitution)
            return super(InstitutionStudentLoginView, self).form_invalid(form)
        
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.user.has_perm('institutions.is_institute'):
                return redirect(reverse_lazy("institutions:dashboard"))
            elif self.request.user.has_perm('staff.is_staff'):
                return redirect(reverse_lazy("staff:dashboard"))
            else:
                return redirect(reverse_lazy("student:dashboard"))

        return super(InstitutionStudentLoginView, self).dispatch(*args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        
        form = self.get_form()
        username = self.request.POST.get('username', '')
        password = self.request.POST.get('password', '')
        
        user = User.objects.filter(username=username).first()
        if user.is_active == False:
            messages.add_message(self.request, messages.ERROR, 'Your Account is Not ACTIVE. Please Contact Us With Your Registered Staff')
        
        return super(InstitutionStudentLoginView, self).post(request, *args, **kwargs)
  

@login_required(login_url="login/")
def dashboard(request):
    #current_institute = Institutions.objects.get(user__username=request.user)
    #license_institute = License.objects.get(li_institute=current_institute)

    #license_form = LicenseViewForm(instance = license_institute)
    
    #card view data=============
    student_obj = Student.objects.get(studentuser = request.user)
    total_obj = Result.objects.filter(registered_user = student_obj,assesment_submitted = True).aggregate(total = Count('assesment_submitted'))
    passed_obj = Result.objects.filter(publish_result = True, registered_user = student_obj,result_passed = True).aggregate(passed = Count('result_passed'))
    pending_obj = Result.objects.filter(publish_result = False, registered_user = student_obj).count()
    total_live_assessment, live_asessment = None, None
    
    all_user_linked_assesment = Assesment.soft_objects.filter(subscriber_users = student_obj, privilege='public')
    all_user_linked_assesment_filter_exam_date = all_user_linked_assesment.filter(exam_start_date_time__lte= make_aware(timezone.datetime.now()), expired_on__gte= make_aware(timezone.datetime.now()))

    if all_user_linked_assesment_filter_exam_date.exists():
        all_user_linked_result = Result.soft_objects.filter(registered_user=student_obj).filter(assesment_submitted=True)
        if all_user_linked_result.exists():
            live_asessment = all_user_linked_assesment_filter_exam_date.exclude(result__in = all_user_linked_result )
        else:
            live_asessment = all_user_linked_assesment_filter_exam_date
    else:
        live_asessment = all_user_linked_assesment_filter_exam_date
        
    total_live_assessment =  live_asessment.count()
    
    total = total_obj['total']
    passed = passed_obj['passed']
    pending = pending_obj
    failed = (total-pending) - passed
 
    
    #graph data=================
    result_obj = Result.objects.filter(publish_result = True, registered_user = student_obj,assesment_submitted = True).values('assesment__header').annotate(obtained_marks = Sum('obtained_marks'),total_marks = Sum('total_marks'),passing_marks = Sum('assesment__passing_marks'))

    
    return render(request, 'student/dashboard.html', {'section': 'dashboard','total':total,'passed':passed,'failed':failed,'pending':pending_obj,'result_obj':result_obj, 'total_live_assessment':total_live_assessment, })
    '''
    from django.http.response import HttpResponse
    return HttpResponse('sddf')
    '''



#password reset through class based
class StudentPasswordResetView(PasswordResetView):
    template_name = 'student/password_reset_form.html'
    email_template_name= 'student/password_reset_email.html'
    success_url = reverse_lazy('student:password_reset_done')


class StudentPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'student/password_reset_done.html'


class StudentPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'student/password_reset_confirm.html'
    success_url = reverse_lazy('student:password_reset_complete')


class StudentPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'student/password_reset_complete.html'


@login_required(login_url="student:login")
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance = request.user, data=request.POST)

        if user_form.is_valid():
            user_form.save()
            messages.add_message(request, messages.SUCCESS, 'Profile Updated Successfully')
        else:
            messages.add_message(request, messages.ERROR, 'Profile Failed To Update')
    else:
        user_form = UserEditForm(instance=request.user)

    return render(request, 'student/edit.html',{  'user_form': user_form})



class PasswordChangeViewForStudent(PasswordChangeView):
    template_name = 'student/password_change.html'
    success_url = reverse_lazy('student:password_change_done')
    
    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(login_required(login_url=reverse_lazy('student:login')))
    def dispatch(self, *args, **kwargs):
        return super(PasswordChangeView, self).dispatch(*args, **kwargs)
        
        
class PasswordChangeDoneViewForStudent(LoginRequiredMixin,PasswordChangeDoneView):
    template_name='student/password_change_done.html'

    @method_decorator(login_required(login_url=reverse_lazy('student:login')))
    def dispatch(self, *args, **kwargs):
        return super(PasswordChangeDoneView, self).dispatch(*args, **kwargs)
    
    
    
class MyIssuedLibraryAsset(LoginRequiredMixin,ListView):
    model = AssetHistory
    template_name = 'student/my_issued_library_asset.html'
    paginate_by = 10
    context_object_name = 'my_issued_library_asset'
    queryset = None
    login_url=reverse_lazy('student:login')
    
    def get_queryset(self,**kwargs):
        student_user = User.objects.get(username = self.request.user)
        student_id = Student.objects.get(studentuser = student_user)
        self.queryset = AssetHistory.objects.filter(student_id=student_id)
        return super(MyIssuedLibraryAsset,self).get_queryset()
    
     
class ViewLibraryAsset(LoginRequiredMixin,FilterView,ListView):
    model = LibraryAsset
    template_name = 'student/view_library_asset.html'
    paginate_by = 10
    context_object_name = 'library_asset'
    queryset = LibraryAsset.objects.all()
    filterset_class = ViewLibraryAssetFilter
    login_url=reverse_lazy('student:login')
    
    
class StudentResult(LoginRequiredMixin,ListView):
    model = Result
    template_name = 'student/student_result.html'
    paginate_by = 10
    context_object_name = 'result'
    #filterset_class = ViewLibraryAssetFilter
    login_url=reverse_lazy('student:login')
    
    
    def get_queryset(self,**kwargs):
        student_obj = Student.objects.get(studentuser = self.request.user)
        self.queryset = Result.objects.filter(publish_result = True, registered_user = student_obj)
        return super(StudentResult,self).get_queryset()
    
 
class ResultReport(LoginRequiredMixin,TemplateView):
    template_name = 'student/student_result_report.html'
    pdf_filename = None
    login_url=reverse_lazy('student:login')
    def get_context_data(self, **kwargs):
        context = super(ResultReport, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        result = Result.objects.get(id=pk)
        student = Student.objects.get(studentuser = self.request.user)
        self.pdf_filename = "Result of {0}({1}).pdf".format(result.assesment.header,student.studentuser.username)
        context['result'] = result
        context['student'] = student
        return context


def authentication_check_decorator(func):

    @wraps(func)
    def check_authentication(self, *args, **kwargs):
            if self.request.user.is_authenticated:
                if self.request.user.has_perm('institutions.is_institute'):
                    return redirect(reverse_lazy("institutions:dashboard"))
                elif self.request.user.has_perm('staff.is_staff'):
                    return redirect(reverse_lazy("staff:dashboard"))
                else:
                    return redirect(reverse_lazy("student:dashboard"))
                    
            return func(self, *args, **kwargs)
                    
    def inner_decoration(self, *args, **kwargs):
        return check_authentication(self, *args, **kwargs)
        
    return inner_decoration

class StudentRegistration(FormView):
    template_name = 'student/student_registration.html'
    form_class = StudentRegistrationForm
    success_url = "/student/login/"
    
   
            
    @authentication_check_decorator
    def dispatch(self, *args, **kwargs):
        return super(StudentRegistration, self).dispatch(*args, **kwargs)
        
    def form_valid(self, form):
        user_obj = form.save()
        staff_obj = Staff.objects.get(id=self.request.POST['staffuser'])
        if staff_obj.auto_active_student == False:
            user_obj.is_active = False
        student_obj = Student()
    
        student_obj.studentuser = user_obj
        student_obj.staffuser = staff_obj
        student_obj.standard = self.request.POST['standard']
        student_obj.address = self.request.POST['address']
        student_obj.student_contact_no = self.request.POST['student_contact_no']
        student_obj.parent_contact_no = self.request.POST['parent_contact_no']
        student_obj.gender = self.request.POST['gender']
        
        student_obj.save()
        user_obj.save()
        messages.add_message(self.request, messages.SUCCESS, 'Your Account Registered Successfully')
        return HttpResponseRedirect(self.get_success_url())
    
    def form_invalid(self, form):
        if 'staffuser' in self.request.POST.keys():
            staff_obj = Staff.objects.get(id=self.request.POST['staffuser'])
            if staff_obj.allowregistration == False:
                messages.add_message(self.request, messages.ERROR, 'Registration Not Allowed!!!')
                return HttpResponseRedirect(reverse_lazy('student:student_registration'))
        return super(StudentRegistration,self).form_invalid(form)
    
    
    
    def get_context_data(self, **kwargs):
        if self.request.method == "POST":
            if 'staffuser' in self.request.POST.keys():
                staff_obj = Staff.objects.get(id=self.request.POST['staffuser'])
                kwargs['staff_obj'] = staff_obj
        return super(StudentRegistration,self).get_context_data(**kwargs)
    
    
    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault('content_type', self.content_type)
        return self.response_class(
            request = self.request,
            template = self.get_template_names(),
            context = context,
            **response_kwargs
        )
    

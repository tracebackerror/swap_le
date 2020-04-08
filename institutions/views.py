
from django.shortcuts import render, redirect
from .models import Institutions
# Create your views here.
from .forms import InstitutionsEditForm, UserEditForm, InstitutionLoginForm,StaffCreateForm,InstitutionRegistrationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login     
from django.contrib.auth.decorators import login_required  #permission_required, resolve_url, settings, six,urlparse,user_passes_test, wraps
from django.contrib.auth.views import PasswordChangeDoneView, PasswordChangeView, LoginView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import ListView,FormView
from institutions.models import Institutions
from staff.models import Staff
from django.contrib.auth.models import User
from django.contrib import messages
from django_tables2 import RequestConfig
from staff.tables import StaffTable
from staff.forms import StaffEditForm
from django.db import transaction
from institutions.forms import StaffProfileForm
from django.contrib.auth.forms import UserCreationForm
from licenses.models import License
from django.contrib.auth.views import (PasswordResetView,PasswordResetDoneView, PasswordResetConfirmView ,PasswordResetCompleteView)
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import PermissionRequiredMixin,LoginRequiredMixin
from guardian.shortcuts import assign_perm
from django.contrib.auth.decorators import permission_required

from django_tables2 import SingleTableView
from django.utils.decorators import method_decorator
from fees.models import FeesInstallment
from .filters import ViewFeesInstallmentFilter
from django_filters.views import FilterView
from students.models import Student
from django.db.models import Count,Q
from assesments.models import Result,Assesment

from datetime import datetime,timedelta
import random, string

def institute_login(request):
    if request.method == 'POST':
        posted_form_data = InstitutionLoginForm(request.POST)
        if posted_form_data.is_valid():
            cd = posted_form_data.cleaned_data
            user = authenticate(username=cd['username'],password=cd['password'])

            if user is not None and user.institutions:
                if user.is_active:
                    login(request,user)
                    return HttpResponse('Authencated')
                else:
                    return HttpResponse('Not Authencated')
            else:
                return HttpResponse('Invalid Login')
    else:
        institute_form = InstitutionLoginForm()
        institution_form = InstitutionsEditForm(instance=request.user.institutions)
        return render(request, 'institutions/login.html', {'form': institute_form})
    pass
    
@permission_required('institutions.is_institute',login_url="/institutions/login/")
@login_required
def edit(request):
    if request.method == 'POST':

        user_form = UserEditForm(instance = request.user,
                        data=request.POST)

        institution_form = InstitutionsEditForm(instance=request.user.institutions, data= request.POST)

        if user_form.is_valid() and institution_form.is_valid():
            user_form.save()

            institution_form.save()
            messages.add_message(request, messages.SUCCESS, 'Profile Updated Successfully')
    else:
        user_form = UserEditForm(instance=request.user)
        institution_form = InstitutionsEditForm(instance=request.user.institutions)

    return render(request, 'institutions/edit.html',{ 'institution_form' : institution_form, 'user_form': user_form})

@permission_required('institutions.is_institute',login_url="/institutions/login/")
@login_required(login_url="/institutions/login/")
def institute_staff_edit(request, username):
    if request.method == 'POST':

        user_form = UserEditForm(instance=User.objects.get(username=username),
                                 data=request.POST)

        #staff_form = StaffEditForm(data=request.POST)
        if user_form.is_valid():
            user_form.save()
            #institution_form.save()
            messages.add_message(request, messages.SUCCESS, 'Staff Profile Updated Successfully')
            return HttpResponseRedirect(reverse_lazy('institutions:manage_staff'))
    else:
        user_form = UserEditForm(instance=User.objects.get(username=username))
        #staff_form = StaffEditForm()

    return render(request, 'institutions/staff_edit.html', {'user_form': user_form})





@transaction.atomic
@permission_required('institutions.is_institute',login_url="/institutions/login/")
@login_required(login_url="/institutions/login/")
def institute_staff_create(request):
    if request.method == 'POST':
        user_form = StaffCreateForm(request.POST)

        current_institute = Institutions.objects.get(user__username = request.user)
        license_institute = License.objects.get(li_institute = current_institute)

        is_allowed =   int(license_institute.li_current_staff) < int(license_institute.li_max_staff)

        if is_allowed and user_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()  # This will load the Profile created by the Signal
            assign_perm('staff.is_staff', user)
            profile_form = Staff()  # Reload the profile form with the profile instance

            profile_form.institute = request.user.institutions
            profile_form.staffuser = user
            profile_form.full_clean()  # Manually clean the form this time. It is implicitly called by "is_valid()" method

            license_institute.li_current_staff += 1
            license_institute.save()
            profile_form.save()  # Gracefully save the form
            messages.add_message(request, messages.SUCCESS, 'Staff Profile Added Successfully')
        else:
            messages.add_message(request, messages.INFO, str(user_form.errors.as_ul()))
    else:
        user_form = StaffCreateForm()
        # profile_form = StaffProfileForm()
    return render(request, 'institutions/staff_create.html', {
        'user_form': user_form

    })

@permission_required('institutions.is_institute',login_url="/institutions/login/")
@login_required(login_url="/institutions/login/")
def institute_staff_delete(request, username):
    information = ''
    current_institute = Institutions.objects.filter(user = request.user)
    license_institute = License.objects.get(li_institute = current_institute)
    if request.method == 'GET' and request.user.institutions.user_type == 'institution':

        information = 'Are you sure you want to delete {} ?'.format(str(username))
    elif request.method == 'POST' and request.user.institutions.user_type == 'institution':
        staff_obj = Staff.objects.get(staffuser__username=username)
        staff_obj.deleted = 'Y'
        license_institute.li_current_staff -= 1
        license_institute.save()
        staff_obj.save()
        information = 'Staff Deleted Successfully. '

    return render(request, 'institutions/staff_delete.html', {'information': [information]})

from licenses.forms import LicenseViewForm

@permission_required('institutions.is_institute',login_url="/institutions/login/")
@login_required(login_url="login/")
def dashboard(request):
    current_institute = Institutions.objects.get(user__username=request.user)
    license_institute = License.objects.get(li_institute=current_institute)

    license_form = LicenseViewForm(instance = license_institute)
    
    #Total Male/Female Student Counting data(Pie Chart)
    total_male = Student.objects.filter(staffuser__institute = current_institute,gender='male').count()
    total_female = Student.objects.filter(staffuser__institute = current_institute,gender='female').count()
    
    #Student Marks in Particular Assessment data(Time-Series Graph)
    all_instituion_assessments = Assesment.objects.filter(subscriber_users__staffuser__institute = current_institute).distinct
    
    if request.method == "POST":
        assessment_id = request.POST['assessment_id']
        if assessment_id:
            result_obj = Result.objects.filter(assesment__id = int(assessment_id)).order_by('id')
            assessment_obj = Assesment.objects.get(id = int(assessment_id))
            return render(request, 'institutions/dashboard.html', {'section': 'dashboard', 'current_details': license_form,'total_male':total_male,'total_female':total_female,'result_obj':result_obj,'assessment_header':assessment_obj.header,'all_instituion_assessments':all_instituion_assessments})
    
    return render(request, 'institutions/dashboard.html', {'section': 'dashboard', 'current_details': license_form,'total_male':total_male,'total_female':total_female,'all_instituion_assessments':all_instituion_assessments})




class PasswordChangeViewForInstitutions(PermissionRequiredMixin, PasswordChangeView):
    template_name = 'institutions/password_change.html'
    success_url = 'done/'
    permission_required = 'institutions.is_institute'
    
    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(login_required(login_url="/institutions/login/"))
    def dispatch(self, *args, **kwargs):
        return super(PasswordChangeView, self).dispatch(*args, **kwargs)
        
        
class PasswordChangeDoneViewForInstitutions(PermissionRequiredMixin, PasswordChangeDoneView):
    template_name='institutions/password_change_done2.html'
    permission_required = 'institutions.is_institute'
    
    @method_decorator(login_required(login_url="/institutions/login/"))
    def dispatch(self, *args, **kwargs):
        return super(PasswordChangeDoneView, self).dispatch(*args, **kwargs)


class InstitutionLoginView(LoginView):
    template_name = 'institutions/login.html'
    
    def form_valid(self, form):
        """Security check complete. Log the user in."""

        if hasattr(form.get_user(), 'institutions') and form.get_user().institutions.user_type=='institution':
            return super(InstitutionLoginView, self).form_valid(form)
        else:
            invalidInstitution = 'Not an Valid Institutions Credentials'
            # if '__all__' in form.errors:
            #     form.errors.update({'__all__': form.errors['__all__'] + [invalidInstitution]})
            # else:
            #     form.errors.update({'__all__': [invalidInstitution]})
            form.add_error(None, invalidInstitution)
            return super(InstitutionLoginView, self).form_invalid(form)
            
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            if self.request.user.has_perm('institutions.is_institute'):
                return redirect(reverse_lazy("institutions:dashboard"))
            elif self.request.user.has_perm('staff.is_staff'):
                return redirect(reverse_lazy("staff:dashboard"))
            else:
                return redirect(reverse_lazy("student:dashboard"))

        return super(InstitutionLoginView, self).dispatch(*args, **kwargs)


def people(request):
    table = StaffTable(Staff.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'institutions/staff.html', {'table': table})


class InstitutionStaffView(PermissionRequiredMixin, SingleTableView, ListView):
    model = Staff
    context_object_name = 'table'
    paginate_by = 10
    template_name = 'institutions/staff.html'
    table_class = StaffTable
    permission_required = 'institutions.is_institute'

    #table_data = Staff.active.filter(institute__user__exact=request.user)

    login_decorator = login_required(login_url="/institutions/login/")


    def get_queryset(self):
        self.queryset = Staff.active.filter(institute__user__exact=self.request.user)
        return super(InstitutionStaffView, self).get_queryset()

    @method_decorator(login_decorator)
    def dispatch(self, *args, **kwargs):
        #assign_perm('institutions.is_institute',self.request.user)
        return super(InstitutionStaffView, self).dispatch(*args, **kwargs)


    '''
    def get_context_data(self, **kwargs):
        global queryset
        context = super(InstitutionStaffView, self).get_context_data(**kwargs)
        context['staffs'] = self.request.user.institutions.staffinstitute.all()
        queryset= self.request.user.institutions.staffinstitute.all()
        return context
    '''

#password reset through class based
class InstitutionPasswordResetView(PasswordResetView):
    template_name = 'institutions/password_reset_form.html'
    email_template_name= 'institutions/password_reset_email.html'
    success_url = reverse_lazy('institutions:password_reset_done')


class InstitutionPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'institutions/password_reset_done.html'


class InstitutionPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'institutions/password_reset_confirm.html'
    success_url = reverse_lazy('institutions:password_reset_complete')


class InstitutionPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'institutions/password_reset_complete.html'
    

class StudentFeesInstallment(PermissionRequiredMixin,LoginRequiredMixin,FilterView,ListView):
    model = FeesInstallment
    context_object_name = 'fees_model'
    template_name="institutions/view_student_fees_installment.html"
    paginate_by = 10
    filterset_class = ViewFeesInstallmentFilter
    login_url = reverse_lazy('institutions:login')
    permission_required = 'institutions.is_institute'
    
    

class InstitutionRegistration(FormView):
    template_name = 'institutions/institution_registration.html'
    form_class = InstitutionRegistrationForm
    success_url = reverse_lazy('institutions:login')
    
    
    def form_valid(self, form):
        user_obj = form.save()
        assign_perm('institutions.is_institute', user_obj)
        user_obj.save()
        institution_obj = Institutions()

        institution_obj.user = user_obj
        institution_obj.institute_name = self.request.POST['institute_name']
        institution_obj.institute_address = self.request.POST['institute_address']
        institution_obj.institute_city = self.request.POST['institute_city']
        institution_obj.institute_state = self.request.POST['institute_state']
        institution_obj.institute_country = self.request.POST['institute_country']
        institution_obj.institute_contact_mobile = self.request.POST['institute_contact_mobile']
        institution_obj.institute_contact_landline = self.request.POST['institute_contact_landline']
        
        license_obj = License()
        institution_obj.save()
        
        license_obj.li_institute = institution_obj
        license_obj.li_key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
        license_obj.li_expiration_date = datetime.now() + timedelta(days=10*365)
        license_obj.li_max_staff = 50
        license_obj.li_max_students = 500
        license_obj.li_max_assesments = 1000
        license_obj.li_current_status = 'acti'
        
        license_obj.save()
        
        #Register Institute as first user:
        
        user_obj.refresh_from_db()  # This will load the Profile created by the Signal
        assign_perm('staff.is_staff', user_obj)
        profile_form = Staff()  # Reload the profile form with the profile instance
        profile_form.institute = user_obj.institutions
        profile_form.staffuser = user_obj
        profile_form.full_clean()  # Manually clean the form this time. It is implicitly called by "is_valid()" method
        license_obj.li_current_staff += 1
        license_obj.save()
        profile_form.save()  # Gracefully save the form
        
        messages.add_message(self.request, messages.SUCCESS, 'Your Account Registered Successfully')
        return HttpResponseRedirect(self.get_success_url())
    
    

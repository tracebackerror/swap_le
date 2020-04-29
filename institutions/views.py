
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
from django_tables2.views import SingleTableMixin
from django_tables2.export.views import ExportMixin

from django.utils.decorators import method_decorator
from fees.models import FeesInstallment
from .filters import ViewFeesInstallmentFilter
from django_filters.views import FilterView
from students.models import Student
from django.db.models import Count,Q
from assesments.models import Result,Assesment

from datetime import datetime,timedelta
import random, string

from swaple.settings import DEFAULT_FROM_EMAIL
from django.core.mail import send_mail
from django.utils.safestring import SafeString
from django.utils.html import format_html

from django.utils import timezone

from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template import loader
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.views.generic import *

from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template import loader
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail

from django.views.generic import *


from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models.query_utils import Q

from django import forms
from django.contrib.auth import (REDIRECT_FIELD_NAME, login as auth_login,
    logout as auth_logout, get_user_model, update_session_auth_hash)
    
class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
        }
    new_password1 = forms.CharField(label=("New password"),
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=("New password confirmation"),
                                    widget=forms.PasswordInput)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                    )
        return password2

class InstitutionPasswordResetView(PasswordResetView):
    template_name = 'institutions/password_reset_form.html'
    email_template_name= 'institutions/password_reset_email.html'
    success_url = reverse_lazy('institutions:password_reset_done')

class PasswordResetConfirmView(FormView):
    template_name = 'institutions/password_reset_confirm.html'
    email_template_name= 'institutions/password_reset_email.html'
    success_url = reverse_lazy('institutions:login')
    form_class = SetPasswordForm

    def post(self, request, uidb64=None, token=None, *arg, **kwargs):
        """
        View that checks the hash in a password reset link and presents a
        form for entering a new password.
        """
        UserModel = get_user_model()
        form = self.form_class(request.POST)
        assert uidb64 is not None and token is not None  # checked by URLconf
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            if form.is_valid():
                new_password= form.cleaned_data['new_password2']
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password has been reset.')
                return self.form_valid(form)
            else:
                messages.error(request, 'Password reset has not been unsuccessful.')
                return self.form_invalid(form)
        else:
            messages.error(request,'The reset password link is no longer valid.')
            return self.form_invalid(form)
            

            
class PasswordResetRequestForm(forms.Form):
    #We are not using EmailField on purpose
    #because you want to treat it
    #as a username if its not an email
    email_or_username = forms.CharField(required=True)

    
        
class ResetPasswordRequestView(FormView):
    template_name = 'institutions/password_reset_form.html'
    email_template_name= 'institutions/password_reset_email.html'
    success_url = reverse_lazy("institutions:login")
    subject_template_name = 'institutions/password_reset_subject.txt'
    
    form_class = PasswordResetRequestForm

    @staticmethod
    def validate_email_address(email):
        '''
        This method here validates the if the input is an email address or not. Its return type is boolean, True if the input is a email address or False if its not.
        '''
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

    def post(self, request, *args, **kwargs):
        '''
        A normal post request which takes input from field "email_or_username" (in ResetPasswordRequestForm).
        '''
        form = self.form_class(request.POST)
        if form.is_valid():
            data= form.cleaned_data["email_or_username"]
        if self.validate_email_address(data) is True:                 #uses the method written above
            '''
            If the input is an valid email address, then the following code will lookup for users associated with that email address. If found then an email will be sent to the address, else an error message will be printed on the screen.
            '''
            associated_users= User.objects.filter(Q(email=data)|Q(username=data))
            if associated_users.exists():
                for user in associated_users:
                        c = {
                            'email': user.email,
                            'domain': 'www.swaple.in',
                            'site_name': 'Swaple',
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'user': user,
                            'token': default_token_generator.make_token(user),
                            'protocol': 'https',
                            }
                        
                        # copied from django/contrib/admin/templates/registration/password_reset_subject.txt to templates directory
                        
                        # copied from django/contrib/admin/templates/registration/password_reset_email.html to templates directory
                        
                        subject = loader.render_to_string(self.subject_template_name, c)
                        # Email subject *must not* contain newlines
                        subject = ''.join(subject.splitlines())
                        email = loader.render_to_string(self.email_template_name, c)
                        send_mail(subject, email, DEFAULT_FROM_EMAIL , [user.email], fail_silently=False)
                result = self.form_valid(form)
                messages.success(request, 'An email has been sent to ' + data +". Please check its inbox to continue reseting password.")
                return redirect(self.success_url)
            result = self.form_invalid(form)
            messages.error(request, 'No user is associated with this email address.')
            return result
        else:
            '''
            If the input is an username, then the following code will lookup for users associated with that user. If found then an email will be sent to the user's address, else an error message will be printed on the screen.
            '''
            associated_users= User.objects.filter(username=data)
            if associated_users.exists():
                for user in associated_users:
                    c = {
                        'email': user.email,
                        'domain': 'www.swaple.in', #or your domain
                        'site_name': 'Swaple',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'user': user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'https',
                        }
                    
                   
                    subject = loader.render_to_string(self.subject_template_name, c)
                    # Email subject *must not* contain newlines
                    subject = ''.join(subject.splitlines())
                    email = loader.render_to_string(self.email_template_name, c)
                    send_mail(subject, email, DEFAULT_FROM_EMAIL , [user.email], fail_silently=False)
                result = self.form_valid(form)
                messages.success(request, 'Email has been sent to ' + data +"'s email address. Please check its inbox to continue reseting password.")
                return redirect(self.success_url)
            result = self.form_invalid(form)
            messages.error(request, 'This username does not exist in the system.')
            return result
        messages.error(request, 'Invalid Input')
        return self.form_invalid(form)
        

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

            
            profile_form.save()  # Gracefully save the form
            messages.add_message(request, messages.SUCCESS, 'Staff {} Added Successfully'.format(request.POST['username']))
            return redirect(reverse_lazy("institutions:manage_staff"))
        '''
        else:
            messages.add_message(request, messages.INFO, str(user_form.errors.as_ul()))
        '''
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
    current_institute = Institutions.objects.filter(user = request.user).first()
    if request.method == 'GET' and request.user.institutions.user_type == 'institution':

        information = 'Are you sure you want to delete {} ?'.format(str(username))
    elif request.method == 'POST' and request.user.institutions.user_type == 'institution':
        staff_obj = Staff.objects.get(staffuser__username=username)
        staff_obj.delete()
        
        information = 'Staff Deleted Successfully. '
        messages.add_message(request, messages.SUCCESS, information)
        return redirect(reverse_lazy("institutions:manage_staff"))

    return render(request, 'institutions/staff_delete.html', {'information': [information]})

from licenses.forms import LicenseViewForm

@permission_required('institutions.is_institute',login_url="/institutions/login/")
@login_required(login_url="login/")
def dashboard(request):
    current_institute = Institutions.objects.get(user__username=request.user)
    license_institute = License.objects.get(li_institute=current_institute)
    
    #License Metrics Update
    student_count = Student.objects.filter(staffuser__institute = current_institute).count()
    staff_count = Staff.objects.filter(institute = current_institute).count()
    assesment_count = Assesment.objects.filter(created_by__username__in = Staff.objects.filter(institute = current_institute).values('staffuser__username')).count()
    License.objects.filter(li_institute=current_institute).update(li_current_staff = staff_count, li_current_students=student_count, li_current_assesments=assesment_count)
    
    
    #license_form = LicenseViewForm(instance = license_institute)
    
    
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
            return render(request, 'institutions/dashboard.html', {'section': 'dashboard', 'current_details': license_institute,'total_male':total_male,'total_female':total_female,'result_obj':result_obj,'assessment_header':assessment_obj.header,'all_instituion_assessments':all_instituion_assessments})
    
    return render(request, 'institutions/dashboard.html', {'section': 'dashboard', 'current_details': license_institute,'total_male':total_male,'total_female':total_female,'all_instituion_assessments':all_instituion_assessments})




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
        if self.request.user.is_authenticated:
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


class InstitutionStaffView(PermissionRequiredMixin, ExportMixin, SingleTableView, ListView):
    export_name =  "Staff Dataset"
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
        license_obj.li_expiration_date = timezone.now() + timedelta(days=10*365)
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
        
        subject = 'Welcome to Swaple - Digital Assessment Platform'
        message = "Dear Sir/Madam, \n\nWelcome to Swaple Digital Assessment Platform. We are so glad to have your institute {} onboarded.\n\n"
        message += "The next step is to add few staff, students and create Assessment. \n\n"
        message += "For any assistance our team is ready to assist you. Please find our team details in signature \n\n"
        message += "Thank you,\n"
        message += "{}\nSupport: {}\nBusiness: {}\n{}"
        message = message.format( 
            self.request.POST['institute_name'].title(),
            "Team Swaple".title(),
            "swapledigital@gmail.com".lower(),
            "admin@swaple.in".lower(),
            "www.swaple.in".lower(),
            )
        #import pdb; pdb.set_trace();
        send_mail(subject, message, DEFAULT_FROM_EMAIL, [self.request.POST['email']], fail_silently = True)
            
        return HttpResponseRedirect(self.get_success_url())
    
    

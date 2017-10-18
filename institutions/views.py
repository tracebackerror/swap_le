
from django.shortcuts import render
from .models import Institutions
# Create your views here.
from .forms import InstitutionsEditForm, UserEditForm, InstitutionLoginForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login     
from django.contrib.auth.decorators import login_required  #permission_required, resolve_url, settings, six,urlparse,user_passes_test, wraps
from django.contrib.auth.views import PasswordChangeDoneView, PasswordChangeView, LoginView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import ListView
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
    else:
        user_form = UserEditForm(instance=User.objects.get(username=username))
        #staff_form = StaffEditForm()

    return render(request, 'institutions/staff_edit.html', {'user_form': user_form})





@transaction.atomic
@login_required(login_url="/institutions/login/")
def institute_staff_create(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)

        current_institute = Institutions.objects.get(user__username = request.user)
        license_institute = License.objects.get(li_institute = current_institute)

        is_allowed =   int(license_institute.li_current_staff) < int(license_institute.li_max_staff)

        if is_allowed and user_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()  # This will load the Profile created by the Signal
            profile_form = Staff()  # Reload the profile form with the profile instance

            profile_form.institute = request.user.institutions
            profile_form.staffuser = user
            profile_form.full_clean()  # Manually clean the form this time. It is implicitly called by "is_valid()" method

            license_institute.li_current_staff += 1
            license_institute.save()
            profile_form.save()  # Gracefully save the form
            messages.add_message(request, messages.SUCCESS, 'Staff Profile Added Successfully')
        else:
            messages.add_message(request, messages.INFO, 'Staff Limit Reached. Kindly Reach to Admin for Upgrade.')
    else:
        user_form = UserCreationForm()
        # profile_form = StaffProfileForm()
    return render(request, 'institutions/staff_create.html', {
        'user_form': user_form

    })


@login_required(login_url="/institutions/login/")
def institute_staff_delete(request, username):
    information = ''
    if request.method == 'GET' and request.user.institutions.user_type == 'institution':

        information = 'Are you sure you want to delete {} ?'.format(str(username))
    elif request.method == 'POST' and request.user.institutions.user_type == 'institution':
        staff_obj = Staff.objects.get(staffuser__username=username)
        staff_obj.deleted = 'Y'
        staff_obj.save()
        information = 'Staff Deleted Successfully. '

    return render(request, 'institutions/staff_delete.html', {'information': [information]})

from licenses.forms import LicenseViewForm
@login_required(login_url="login/")
def dashboard(request):
    current_institute = Institutions.objects.get(user__username=request.user)
    license_institute = License.objects.get(li_institute=current_institute)

    license_form = LicenseViewForm(instance = license_institute)

    return render(request, 'institutions/dashboard.html', {'section': 'dashboard', 'current_details': license_form })




class PasswordChangeViewForInstitutions(PasswordChangeView):
    template_name = 'institutions/password_change.html'
    success_url = 'done/'
    
    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(login_required(login_url="/institutions/login/"))
    def dispatch(self, *args, **kwargs):
        return super(PasswordChangeView, self).dispatch(*args, **kwargs)
        
        
class PasswordChangeDoneViewForInstitutions(PasswordChangeDoneView):
    template_name='institutions/password_change_done2.html'

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


def people(request):
    table = StaffTable(Staff.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'institutions/staff.html', {'table': table})

from django_tables2 import SingleTableView
from django.utils.decorators import method_decorator


class InstitutionStaffView(SingleTableView, ListView):
    model = Staff
    context_object_name = 'table'
    paginate_by = 3
    template_name = 'institutions/staff.html'
    table_class = StaffTable
    #table_data = Staff.active.filter(institute__user__exact=request.user)

    login_decorator = login_required(login_url="/institutions/login/")


    def get_queryset(self):
        self.queryset = Staff.active.filter(institute__user__exact=self.request.user)
        return super(InstitutionStaffView, self).get_queryset()

    @method_decorator(login_decorator)
    def dispatch(self, *args, **kwargs):
        return super(InstitutionStaffView, self).dispatch(*args, **kwargs)


    '''
    def get_context_data(self, **kwargs):
        global queryset
        context = super(InstitutionStaffView, self).get_context_data(**kwargs)
        context['staffs'] = self.request.user.institutions.staffinstitute.all()
        queryset= self.request.user.institutions.staffinstitute.all()
        return context
    '''



from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required  #permission_required, resolve_url, settings, six,urlparse,user_passes_test, wraps
from django.contrib.auth.views import PasswordChangeDoneView, PasswordChangeView, LoginView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.urls import reverse_lazy
from django.contrib import messages
from institutions.forms import UserEditForm
from django.views.generic import ListView
from django.contrib.auth import login as auth_login

from django.contrib.auth.views import (PasswordResetView,PasswordResetDoneView, PasswordResetConfirmView ,PasswordResetCompleteView)
from django.urls import reverse_lazy


from .models import Student

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



@login_required(login_url="login/")
def dashboard(request):
    #current_institute = Institutions.objects.get(user__username=request.user)
    #license_institute = License.objects.get(li_institute=current_institute)

    #license_form = LicenseViewForm(instance = license_institute)

    return render(request, 'student/dashboard.html', {'section': 'dashboard'})
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


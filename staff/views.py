from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required  #permission_required, resolve_url, settings, six,urlparse,user_passes_test, wraps
from django.contrib.auth.views import PasswordChangeDoneView, PasswordChangeView, LoginView
from django.urls import reverse_lazy


class InstitutionStaffLoginView(LoginView):
    template_name = 'staff/login.html'

    def form_valid(self, form):
        """Security check complete. Log the user in."""

        if hasattr(form.get_user(), 'staff') and (form.get_user().staff.user_type == 'staff'):
            return super(InstitutionStaffLoginView, self).form_valid(form)
        else:
            invalidInstitution = 'Not an Valid Staff Credentials'
            # if '__all__' in form.errors:
            #     form.errors.update({'__all__': form.errors['__all__'] + [invalidInstitution]})
            # else:
            #     form.errors.update({'__all__': [invalidInstitution]})
            form.add_error(None, invalidInstitution)
            return super(InstitutionStaffLoginView, self).form_invalid(form)


@login_required(login_url="login/")
def dashboard(request):
    #current_institute = Institutions.objects.get(user__username=request.user)
    #license_institute = License.objects.get(li_institute=current_institute)

    #license_form = LicenseViewForm(instance = license_institute)

    return render(request, 'staff/dashboard.html', {'section': 'dashboard'})
    '''
    from django.http.response import HttpResponse
    return HttpResponse('sddf')
    '''
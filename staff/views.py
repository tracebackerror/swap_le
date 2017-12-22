from django.http.response import HttpResponse
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

from staff.forms import StudentEditForm, StudentUserEditForm 
from students.models import Student
from django.contrib.auth.models import User
#from jedi.evaluate.context import instance

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

@login_required(login_url=reverse_lazy('staff:login'))
def edit(request):
    if request.method == 'POST':

        user_form = UserEditForm(instance = request.user,
                        data=request.POST)

#         institution_form = InstitutionsEditForm(instance=request.user.institutions, data= request.POST)

        if user_form.is_valid():
            user_form.save()
#             institution_form.save()
            messages.add_message(request, messages.SUCCESS, 'Profile Updated Successfully')
        else:
            messages.add_message(request, messages.ERROR, 'Profile Failed To Update')
    else:
        user_form = UserEditForm(instance=request.user)
#         institution_form = InstitutionsEditForm(instance=request.user.institutions)

    return render(request, 'staff/edit.html',{  'user_form': user_form})



class PasswordChangeViewForStaff(PasswordChangeView):
    template_name = 'staff/password_change.html'
    success_url = reverse_lazy('staff:password_change_done')
    
    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(login_required(login_url=reverse_lazy('staff:login')))
    def dispatch(self, *args, **kwargs):
        return super(PasswordChangeView, self).dispatch(*args, **kwargs)
        
        
class PasswordChangeDoneViewForStaff(PasswordChangeDoneView):
    template_name='staff/password_change_done2.html'

    @method_decorator(login_required(login_url=reverse_lazy('staff:login')))
    def dispatch(self, *args, **kwargs):
        return super(PasswordChangeDoneView, self).dispatch(*args, **kwargs)



from django_tables2 import SingleTableView
from django.utils.decorators import method_decorator
from students.models import Student
from staff.tables import StudentTable
from staff.forms import EnrollStudentsForm
from staff.models import Staff
from students.models import Student

class ManageStudentView(SingleTableView, ListView):
    model = Student
    context_object_name = 'table'
    paginate_by = 3
    template_name = 'staff/manage_student.html'
    table_class = StudentTable
    
    #table_data = Staff.active.filter(institute__user__exact=request.user)

    login_decorator = login_required(login_url=reverse_lazy('staff:login'))


    def get_queryset(self):
        get_associated_staff = Staff.active.filter(staffuser=self.request.user)
        self.queryset = Student.active.filter(staffuser = get_associated_staff)#active.filter(institute__user__exact=self.request.user)
        return super(ManageStudentView, self).get_queryset()

    @method_decorator(login_decorator)
    def dispatch(self, *args, **kwargs):
        return super(ManageStudentView, self).dispatch(*args, **kwargs)


    
    def get_context_data(self, **kwargs):
        context = super(ManageStudentView, self).get_context_data(**kwargs)
       
        return context
    
    
@login_required(login_url="/staff/login/")
def delete_institution_staff_student(request, username):
    information = ''
    
    if hasattr(request.user, 'staff'):
        if request.method == 'GET' and request.user.staff.user_type in ['staff','institution']:
            information = 'Are you sure you want to delete user {} ?'.format(str(username))
        elif request.method == 'POST' and request.user.staff.user_type == 'staff':
            staff_obj = Staff.objects.get(staffuser__username=request.user)
            student_obj = Student.active.get(studentuser__username__exact=username)
            #student_obj = Student.objects.get(staffuser = staff_obj)
            if student_obj in staff_obj.student_set.all():
                student_obj.deleted = 'Y'
                student_obj.save()
                information = 'Student Deleted Successfully. '
        return render(request, 'staff/student_delete.html', {'information': [information]})
    else:
        #latter implementation of this bug
        pass


#implementing edit functionality     
@login_required(login_url="/staff/login/")
def student_edit_by_staff(request,upk):
    if request.method == 'POST':
        student_form = StudentEditForm(instance=Student.objects.get(pk=upk),
                                 data=request.POST)
        if student_form.is_valid():
            student_form.save()
            messages.add_message(request, messages.SUCCESS, 'Student Record Updated Successfully')
            
    else:
        student_form = StudentEditForm(instance=Student.objects.get(pk=upk)) 
        
    return render(request, 'staff/student_edit_by_staff.html', {'student_form': student_form})


#implementing edit functionality     
@login_required(login_url="/staff/login/")
def student_edit_by_staff(request,upk):
    if request.method == 'POST':
        student_form = StudentEditForm(instance=Student.objects.get(pk=upk),
                                 data=request.POST)
        student_user_form = StudentUserEditForm(instance=User.objects.get(id=student_form.instance.studentuser.id),
                                 data=request.POST)
        if student_form.is_valid() and student_user_form.is_valid():
            student_form.save()
            student_user_form.save()
            messages.add_message(request, messages.SUCCESS, 'Student Record Updated Successfully')
            
    else:
        student_data=Student.objects.get(pk=upk)
        student_form = StudentEditForm(instance=student_data)
        student_user_form = StudentUserEditForm(instance=User.objects.get(pk=student_form.instance.studentuser.id))
        
    return render(request, 'staff/student_edit_by_staff.html', {'student_form': student_form,'student_user_form': student_user_form})

   
    
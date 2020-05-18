from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeDoneView, PasswordChangeView, LoginView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.urls import reverse_lazy
from django.contrib import messages
from institutions.forms import UserEditForm
from django.views.generic import ListView,TemplateView,DeleteView,UpdateView
from django.contrib.auth.decorators import permission_required
from staff.forms import StudentEditForm,StudentUserEditForm,CreateStudentEnquiryForm
from licenses.models import License
from django.contrib.auth.models import User
from django.contrib.auth.views import (PasswordResetView,PasswordResetDoneView, PasswordResetConfirmView ,PasswordResetCompleteView)

from django.contrib.auth.mixins import PermissionRequiredMixin,LoginRequiredMixin
from guardian.shortcuts import assign_perm

from django_tables2 import SingleTableView
from django_tables2.views import SingleTableMixin
from django_tables2.export.views import ExportMixin

from django.utils.decorators import method_decorator
from staff.tables import StudentTable
from staff.forms import EnrollStudentsForm,StudentAddForm
from staff.models import Staff,StudentEnquiry
from students.models import Student
from django.views.generic.edit import FormView
#from jedi.evaluate.context import instance
from .filters import StudentEnquiryFilter
from django_filters.views import FilterView
from django.urls import reverse

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LogoutView   

class StaffLogout(SuccessMessageMixin, LogoutView):
    next_page = reverse_lazy('staff:login')
    success_message = 'You are succesfully logged out.'

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
            
            
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.user.has_perm('institutions.is_institute'):
                return redirect(reverse_lazy("institutions:dashboard"))
            elif self.request.user.has_perm('staff.is_staff'):
                return redirect(reverse_lazy("staff:dashboard"))
            else:
                return redirect(reverse_lazy("student:dashboard"))

        return super(InstitutionStaffLoginView, self).dispatch(*args, **kwargs)

            
@permission_required('staff.is_staff',login_url=reverse_lazy('staff:login'))
@login_required(login_url=reverse_lazy('staff:login'))
def dashboard(request):
    #current_institute = Institutions.objects.get(user__username=request.user)
    #license_institute = License.objects.get(li_institute=current_institute)

    #license_form = LicenseViewForm(instance = license_institute)
    
    #Total Male/Female Student Counting data
    current_institute = Staff.objects.get(staffuser = request.user).institute
    total_male = Student.objects.filter(staffuser__institute = current_institute,gender='male').count()
    total_female = Student.objects.filter(staffuser__institute = current_institute,gender='female').count()

    return render(request, 'staff/dashboard.html', {'section': 'dashboard','total_male':total_male,'total_female':total_female})
    '''
    from django.http.response import HttpResponse
    return HttpResponse('sddf')
    '''

@permission_required('staff.is_staff',login_url=reverse_lazy('staff:login'))
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





class ManageStudentView(PermissionRequiredMixin, ExportMixin, SingleTableView, ListView):
    export_name =  "Student Dataset"
    model = Student
    context_object_name = 'table'
    paginate_by = 20
    template_name = 'staff/manage_student.html'
    table_class = StudentTable
    permission_required = 'staff.is_staff'
    
    #table_data = Staff.active.filter(institute__user__exact=request.user)

    login_decorator = login_required(login_url=reverse_lazy('staff:login'))


    def get_queryset(self):
        get_associated_staff = Staff.active.filter(staffuser=self.request.user)
        self.queryset = Student.active.filter(staffuser__in = get_associated_staff)#active.filter(institute__user__exact=self.request.user)
        return super(ManageStudentView, self).get_queryset()

    @method_decorator(login_decorator)
    def dispatch(self, *args, **kwargs):
        return super(ManageStudentView, self).dispatch(*args, **kwargs)

    
    def get_context_data(self, **kwargs):
        context = super(ManageStudentView, self).get_context_data(**kwargs)
        context['allow_registration']=1 if self.request.user.staff.allowregistration else 0
        context['auto_active_student']=1 if self.request.user.staff.auto_active_student else 0
        
        return context
    
    
    def post(self, request, *args, **kwargs):
        if request.is_ajax():               
            if request.method == "POST":
                student_reg = request.POST.get('student_reg')
                auto_active = request.POST.get('auto_active')
                staff_obj = Staff.objects.get(id=self.request.user.staff.id)
                staff_obj.allowregistration = 1 if student_reg == "true" else 0
                staff_obj.auto_active_student = 1 if auto_active == "true" else 0
                staff_obj.save()
        return super(ManageStudentView,self).get(request, *args, **kwargs)
    
    
   
    
    
@permission_required('staff.is_staff',login_url=reverse_lazy('staff:login'))
@login_required(login_url=reverse_lazy('staff:login'))
def delete_institution_staff_student(request, username):
    information = ''
    current_staff = Staff.objects.get(staffuser = request.user)
    license_institute = License.objects.get(li_institute = current_staff.institute)
    if hasattr(request.user, 'staff'):
        if request.method == 'GET' and request.user.staff.user_type in ['staff','institution']:
            information = 'Are you sure you want to delete user {} ?'.format(str(username))
        elif request.method == 'POST' and request.user.staff.user_type == 'staff':
            staff_obj = Staff.objects.get(staffuser__username=request.user)
            student_obj = Student.active.get(studentuser__username__exact=username)
            #student_obj = Student.objects.get(staffuser = staff_obj)
            if student_obj in staff_obj.student_set.all():
                student_obj.deleted = 'Y'
                license_institute.li_current_students -= 1
                license_institute.save()
                student_obj.save()
                information = 'Student Deleted Successfully. '
        return render(request, 'staff/student_delete.html', {'information': [information]})
    else:
        #latter implementation of this bug
        pass


@permission_required('staff.is_staff',login_url=reverse_lazy('staff:login'))
@login_required(login_url=reverse_lazy('staff:login'))
def student_edit_by_staff(request,upk):
    student_data=Student.objects.get(pk=upk)
    if request.method == 'POST':
        student_form = StudentEditForm(instance=Student.objects.get(id=upk),data=request.POST)
        student_user_form = StudentUserEditForm(instance=User.objects.get(id=student_data.studentuser.id),data=request.POST)
        if student_form.is_valid() and student_user_form.is_valid():
            student_form.save()
            student_user_form.save()
            messages.add_message(request, messages.SUCCESS, 'Student Record Updated Successfully')
            return HttpResponseRedirect(reverse('staff:manage_student'))
            
    else:
        student_form = StudentEditForm(instance=Student.objects.get(id=upk))
        student_user_form = StudentUserEditForm(instance=User.objects.get(id=student_data.studentuser.id))
    return render(request, 'staff/student_edit_by_staff.html', {'student_form':student_form,'student_user_form': student_user_form})


@permission_required('staff.is_staff',login_url=reverse_lazy('staff:login'))
@login_required(login_url=reverse_lazy('staff:login'))
def add_student_by_staff(request):
    current_staff = Staff.objects.get(staffuser = request.user)
    if current_staff.allowregistration==True:
        if request.method == 'POST':
            add_student_form = StudentAddForm(request.POST)
    
            #current_staff = Staff.objects.get(staffuser = request.user)
            license_institute = License.objects.get(li_institute = current_staff.institute)
    
            is_allowed =   int(license_institute.li_current_students) < int(license_institute.li_max_students)
    
            if is_allowed:
                if add_student_form.is_valid():
                    user=add_student_form.save()
                    standard=request.POST['standard']
                    address=request.POST['address']
                    student_contact_no=request.POST['student_contact_no']
                    parent_contact_no=request.POST['parent_contact_no']
                    gender = request.POST['gender']
                    
                    student_profile=Student.objects.create(studentuser=user,staffuser=request.user.staff,deleted='N',standard=standard,address=address,student_contact_no=student_contact_no,parent_contact_no=parent_contact_no,gender=gender)
                    
                    license_institute.li_current_students += 1
                    student_profile.save()
                    license_institute.save()
                    messages.add_message(request, messages.SUCCESS, 'Student Profile Added Successfully')
                    return HttpResponseRedirect(reverse_lazy('staff:manage_student'))
            else:
                messages.add_message(request, messages.INFO, 'Staff Limit Reached. Kindly Reach to Admin for Upgrade.')
        else:
            add_student_form = StudentAddForm()
        return render(request, 'staff/add_student_by_staff.html', {'form': add_student_form})
    else:
        return render(request, 'staff/display_messege_staff.html')
    

#password reset through class based
class StaffPasswordResetView(PasswordResetView):
    template_name = 'staff/password_reset_form.html'
    email_template_name= 'staff/password_reset_email.html'
    success_url = reverse_lazy('staff:password_reset_done')


class StaffPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'staff/password_reset_done.html'


class StaffPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'staff/password_reset_confirm.html'
    success_url = reverse_lazy('staff:password_reset_complete')


class StaffPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'staff/password_reset_complete.html'
    

class CreateStudentEnquiryView(PermissionRequiredMixin,LoginRequiredMixin,FormView):
    template_name="staff/create_student_enquiry.html"
    form_class = CreateStudentEnquiryForm 
    success_url = '/staff/'
    http_method_names = ['post','get']
    login_url=reverse_lazy('staff:login')
    permission_required = 'staff.is_staff'
    

    def form_valid(self, form):
        if super().form_valid(form):
            obj=User.objects.get(username=self.request.user)            
            created_by=Staff.objects.get(staffuser=obj)
            full_name=form.cleaned_data['full_name']
            parent_name=form.cleaned_data['parent_name']
            scl_clg_name=form.cleaned_data['scl_clg_name']
            std=form.cleaned_data['std']
            academic_y=form.cleaned_data['academic_y']
            contact=form.cleaned_data['contact']
            
            StudentEnquiry.objects.create(created_by=created_by,full_name=full_name,parent_name=parent_name,scl_clg_name=scl_clg_name,std=std,academic_y=academic_y,contact=contact)
            
            messages.add_message(self.request, messages.SUCCESS, 'Enquiry Record Successfully!')
        return super(CreateStudentEnquiryView,self).form_valid(form)
    

class ManageStudentEnquiryView(PermissionRequiredMixin,LoginRequiredMixin,FilterView,ListView):
    model = StudentEnquiry
    context_object_name = 'enquiry_model'
    template_name="staff/manage_student_enquiry.html"
    paginate_by = 10
    login_url=reverse_lazy('staff:login')
    filterset_class=StudentEnquiryFilter
    permission_required = 'staff.is_staff'
    
class DeleteStudentEnquiryView(PermissionRequiredMixin,LoginRequiredMixin,DeleteView):
    model = StudentEnquiry
    pk_url_kwarg = 'pk'
    template_name = "staff/delete_student_enquiry.html"
    context_object_name = 'enquiry'
    success_url=reverse_lazy('staff:manage_student_enquiry')
    login_url=reverse_lazy('staff:login')
    permission_required = 'staff.is_staff'
    

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.add_message(self.request, messages.SUCCESS, 'Deleted Student Enquiry Record Successfully!')
        return HttpResponseRedirect(success_url)
    
class UpdateStudentEnquiryView(PermissionRequiredMixin,LoginRequiredMixin,UpdateView):
    model = StudentEnquiry
    form_class = CreateStudentEnquiryForm  
    pk_url_kwarg = 'pk'
    http_method_names = ['post','get']
    template_name = "staff/update_student_enquiry.html"
    context_object_name = 'form'
    success_url=reverse_lazy('staff:manage_student_enquiry')
    login_url=reverse_lazy('staff:login')
    permission_required = 'staff.is_staff'
    

    def form_valid(self, form):
        if super().form_valid(form):
            form.save()
            messages.add_message(self.request, messages.SUCCESS, 'Updated Student Enquiry Record Successfully!')
        return HttpResponseRedirect(self.get_success_url())
    
    
    

#Student Activate Deactivate View
@login_required(login_url=reverse_lazy('staff:login'))
def StudentActivateDeactivate(request,pk):
    student_obj = Student.objects.get(id=1)
    if student_obj.studentuser.is_active:
        student_obj.studentuser.is_active = False
    else:
        student_obj.studentuser.is_active = True
    student_obj.studentuser.save()
    return HttpResponseRedirect(reverse_lazy("staff:manage_student"))




    
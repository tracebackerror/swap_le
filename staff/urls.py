from django.conf.urls import url, include
from django.contrib.auth.views import LoginView, LogoutView, logout_then_login, PasswordChangeDoneView
#from .views import InstitutionStaffLoginView, dashboard, edit, PasswordChangeViewForStaff, PasswordChangeDoneViewForStaff, ManageStudentView, delete_institution_staff_student, student_edit_by_staff,add_student_by_staff
from .views import *


urlpatterns = [
    url(r'^login/',  InstitutionStaffLoginView.as_view(), name='login'),
    url(r'^$', dashboard, name='dashboard'),
    url(r'^logout/$',  LogoutView.as_view(template_name='staff/logged_out.html'), name='logout'),
    url(r'^edit/$', edit, name="edit"),
    url(r'^password-change/$',PasswordChangeViewForStaff.as_view(), name='password_change'),
    url(r'^password-change/done/$',PasswordChangeDoneViewForStaff.as_view(), name='password_change_done'),
    url(r'^manage/student/$', ManageStudentView.as_view(), name='manage_student'),
    url(r'^manage/student/add-student/', add_student_by_staff, name='add_student'),
    url(r'^manage/student/(?P<username>\w{0,15})/delete/$', delete_institution_staff_student, name='delete_institution_staff_student'),
    url(r'^manage/', include('assesments.urls', namespace='assesments', app_name='assesments')),
    url(r'^manage/student/(?P<upk>\w{0,15})/edit/$', student_edit_by_staff, name='student_edit_by_staff'),
    
#password reset through email
    url(r'^password_reset/$',StaffPasswordResetView.as_view(),name='password_reset'),
    url(r'^password_reset/done/$',StaffPasswordResetDoneView.as_view(),name='password_reset_done'),
    url(r'^reset/done/$',StaffPasswordResetCompleteView.as_view(),name='password_reset_complete'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        StaffPasswordResetConfirmView.as_view(),name='password_reset_confirm'),    

#  Studnet Enquiry     
    url(r'^enquiry/create/',CreateStudentEnquiryView.as_view(), name='create_student_enquiry'),
    url(r'^enquiry/manage/',ManageStudentEnquiryView.as_view(), name='manage_student_enquiry'),
    url(r'^enquiry/(?P<pk>\d+)/delete/$',DeleteStudentEnquiryView.as_view(), name='delete_student_enquiry'),
    url(r'^enquiry/(?P<pk>\d+)/update/$',UpdateStudentEnquiryView.as_view(), name='update_student_enquiry'),
    
    
# Library
    url(r'^library/', include('library.urls', namespace='library', app_name='library')),
    
# Fees
    url(r'^fees/', include('fees.urls', namespace='fees', app_name='fees')),  

]

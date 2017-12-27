from django.conf.urls import url, include
from django.contrib.auth.views import LoginView, LogoutView, logout_then_login, PasswordChangeDoneView
from .views import InstitutionStaffLoginView, dashboard, edit, PasswordChangeViewForStaff, PasswordChangeDoneViewForStaff, ManageStudentView, delete_institution_staff_student, student_edit_by_staff,add_student_by_staff



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
    ]

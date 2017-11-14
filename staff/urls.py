from django.conf.urls import url, include
from django.contrib.auth.views import LoginView, LogoutView, logout_then_login, PasswordChangeDoneView
from .views import InstitutionStaffLoginView, dashboard, edit, delete_institution_staff_student, PasswordChangeViewForStaff, PasswordChangeDoneViewForStaff, ManageStudentView



urlpatterns = [
    url(r'^login/',  InstitutionStaffLoginView.as_view(), name='login'),
    url(r'^$', dashboard, name='dashboard'),
    url(r'^logout/$',  LogoutView.as_view(template_name='staff/logged_out.html'), name='logout'),
    url(r'^edit/$', edit, name="edit"),
    url(r'^password-change/$',PasswordChangeViewForStaff.as_view(), name='password_change'),
    url(r'^password-change/done/$',PasswordChangeDoneViewForStaff.as_view(), name='password_change_done'),
    url(r'^manage/student/$', ManageStudentView.as_view(), name='manage_student'),
    url(r'^manage/student/(?P<username>\w{0,15})/delete/$', delete_institution_staff_student, name='delete_institution_staff_student'),
    url(r'^manage/', include('assesments.urls', namespace='assesments', app_name='assesments'))
    ]

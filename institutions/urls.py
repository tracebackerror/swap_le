from django.conf.urls import url
from .views import edit, institute_staff_edit, dashboard, PasswordChangeViewForInstitutions,\
    PasswordChangeDoneViewForInstitutions, InstitutionLoginView, InstitutionStaffView, \
    institute_staff_delete, institute_staff_create

from django.contrib.auth.views import LoginView, LogoutView, logout_then_login, PasswordChangeDoneView


    
urlpatterns = [
    url(r'^edit/$', edit, name="edit"),
    # url(r'^login/$', institute_login, name='login'), 
    url(r'^login/',  InstitutionLoginView.as_view(), name='login'),
    url(r'^logout/$',  LogoutView.as_view(template_name='institutions/logged_out.html'), name='logout'),
    url(r'^logout-then-login/$', logout_then_login,name='logout_then_login'), 
    url(r'^$', dashboard, name='dashboard'), 
    url(r'^password-change/$',PasswordChangeViewForInstitutions.as_view(), name='password_change'),
    url(r'^password-change/done/$',PasswordChangeDoneViewForInstitutions.as_view(), name='password_change_done'),
    url(r'^manage/staff/$', InstitutionStaffView.as_view(), name='manage_staff'),
    url(r'^manage/staff/(?P<username>\w{0,15})/edit/$', institute_staff_edit, name='edit_institution_staff'),
    url(r'^manage/staff/(?P<username>\w{0,15})/delete/$', institute_staff_delete, name='delete_institution_staff'),
    url(r'^manage/staff/create/$', institute_staff_create, name='create_institution_staff'),
]

from django.conf.urls import url
from .views import *

from django.contrib.auth.views import LoginView, LogoutView, logout_then_login, PasswordChangeDoneView


app_name='institutions'

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
    url(r'^manage/staff/(?P<username>[\w.@+-]+)/edit/$', institute_staff_edit, name='edit_institution_staff'),
    url(r'^manage/staff/(?P<username>[\w.@+-]+)/delete/$', institute_staff_delete, name='delete_institution_staff'),
    url(r'^manage/staff/create/$', institute_staff_create, name='create_institution_staff'),
    
    #password reset through email
    url(r'^password_reset/$',InstitutionPasswordResetView.as_view(),name='password_reset'),
    url(r'^password_reset/done/$',InstitutionPasswordResetDoneView.as_view(),name='password_reset_done'),
    url(r'^reset/done/$',InstitutionPasswordResetCompleteView.as_view(),name='password_reset_complete'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        InstitutionPasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    
    
    #fees installment
    url(r'^fees-installment/view/$',StudentFeesInstallment.as_view(),name='view_student_fees_installment'),
    
    #institution registration
    url(r'^registration/$',InstitutionRegistration.as_view(),name='institution_registration'),
]

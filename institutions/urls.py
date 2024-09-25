from django.urls import path, re_path
from .views import *
from django.contrib.auth.views import LoginView, LogoutView, logout_then_login, PasswordChangeDoneView

app_name = 'institutions'

urlpatterns = [
    path('edit/', edit, name='edit'),
    path('login/', InstitutionLoginView.as_view(), name='login'),
    path('logout/', InstituteLogout.as_view(), name='logout'),
    path('logout-then-login/', logout_then_login, name='logout_then_login'),
    path('', dashboard, name='dashboard'),
    path('password-change/', PasswordChangeViewForInstitutions.as_view(), name='password_change'),
    path('password-change/done/', PasswordChangeDoneViewForInstitutions.as_view(), name='password_change_done'),
    path('manage/staff/', InstitutionStaffView.as_view(), name='manage_staff'),
    path('manage/staff/<username>/edit/', institute_staff_edit, name='edit_institution_staff'),
    path('manage/staff/<username>/delete/', institute_staff_delete, name='delete_institution_staff'),
    path('manage/staff/create/', institute_staff_create, name='create_institution_staff'),
    
    # Password reset through email
    path('password_reset/', ResetPasswordRequestView.as_view(), name='password_reset'),
    path('password_reset/done/', InstitutionPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/done/', InstitutionPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    
    # Fees installment
    path('fees-installment/view/', StudentFeesInstallment.as_view(), name='view_student_fees_installment'),
    
    # Institution registration
    path('registration/', InstitutionRegistration.as_view(), name='institution_registration'),
]

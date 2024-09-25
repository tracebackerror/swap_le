from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from .views import *
from institutions.views import ResetPasswordRequestView, PasswordResetConfirmView

app_name = 'staff'
urlpatterns = [
    path('login/', InstitutionStaffLoginView.as_view(), name='login'),
    path('', dashboard, name='dashboard'),
    path('logout/', StaffLogout.as_view(), name='logout'),
    path('edit/', edit, name='edit'),
    path('password-change/', PasswordChangeViewForStaff.as_view(), name='password_change'),
    path('password-change/done/', PasswordChangeDoneViewForStaff.as_view(), name='password_change_done'),
    path('manage/student/', ManageStudentView.as_view(), name='manage_student'),
    path('manage/student/add-student/', add_student_by_staff, name='add_student'),
    path('manage/student/<username>/delete/', delete_institution_staff_student, name='delete_institution_staff_student'),
    path('manage/', include('assesments.urls', namespace='assesments')),
    path('manage/student/<upk>/edit/', student_edit_by_staff, name='student_edit_by_staff'),

    # Password reset through email
    path('password_reset/', ResetPasswordRequestView.as_view(success_url=reverse_lazy("staff:login")), name='password_reset'),
    path('password_reset/done/', StaffPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/done/', StaffPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('reset/<uidb64>/<token>/', StaffPasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    # Student Enquiry
    path('enquiry/create/', CreateStudentEnquiryView.as_view(), name='create_student_enquiry'),
    path('enquiry/manage/', ManageStudentEnquiryView.as_view(), name='manage_student_enquiry'),
    path('enquiry/<pk>/delete/', DeleteStudentEnquiryView.as_view(), name='delete_student_enquiry'),
    path('enquiry/<pk>/update/', UpdateStudentEnquiryView.as_view(), name='update_student_enquiry'),

    # Library
    path('library/', include('library.urls', namespace='library')),

    # Fees
    path('fees/', include('fees.urls', namespace='fees')),

    # Student Activate/Deactivate
    path('activate-deactivate/<pk>/', StudentActivateDeactivate, name='student_activate_deactivate'),
]

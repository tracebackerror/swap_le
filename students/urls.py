from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeDoneView
from .views import (
    InstitutionStudentLoginView, dashboard, edit, StudentLogout,
    PasswordChangeViewForStudent, PasswordChangeDoneViewForStudent,
    StudentPasswordResetDoneView, StudentPasswordResetCompleteView,
    StudentPasswordResetConfirmView, MyIssuedLibraryAsset, ViewLibraryAsset,
    StudentResult, ResultReport, StudentRegistration
)
from assesments.views import AssessmentResultByStaff, process_open_assessment, ProcessOpenAssesmentView
from institutions.views import ResetPasswordRequestView

app_name = 'student'

urlpatterns = [
    path('login/', InstitutionStudentLoginView.as_view(), name='login'),
    path('', dashboard, name='dashboard'),
    path('edit/', edit, name='edit'),
    path('open/process/', ProcessOpenAssesmentView.as_view(), name='process_new_assesment'),
    path('logout/', StudentLogout.as_view(), name='logout'),
    path('password-change/', PasswordChangeViewForStudent.as_view(), name='password_change'),
    path('password-change/done/', PasswordChangeDoneViewForStudent.as_view(), name='password_change_done'),
    path('', include('assesments.urls', namespace='assesments')),

    # Password reset through email
    path('password_reset/', ResetPasswordRequestView.as_view(success_url='student:login'), name='password_reset'),
    path('password_reset/done/', StudentPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/done/', StudentPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('reset/<uidb64>/<token>/', StudentPasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    # Library
    path('library-asset/my-issued/', MyIssuedLibraryAsset.as_view(), name='my_issued_library_asset'),
    path('library-asset/view/', ViewLibraryAsset.as_view(), name='view_library_asset'),

    # Result
    path('result/', StudentResult.as_view(), name='result'),
    path('result/<int:pk>/report.pdf/', ResultReport.as_view(), name='result_report'),
    path('result/<int:pk>/report/', AssessmentResultByStaff.as_view(), name='result_report_detailed'),

    # Student registration
    path('registration/', StudentRegistration.as_view(), name='student_registration'),
]

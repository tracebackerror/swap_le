from django.conf.urls import url, include
from django.contrib.auth.views import LoginView, LogoutView, logout_then_login, PasswordChangeDoneView
#from .views import InstitutionStudentLoginView, dashboard, edit, PasswordChangeViewForStudent, PasswordChangeDoneViewForStudent
from .views import *

#, dashboard, edit, delete_institution_staff_student, PasswordChangeViewForStaff, PasswordChangeDoneViewForStaff, ManageStudentView





urlpatterns = [
    url(r'^login/',  InstitutionStudentLoginView.as_view(), name='login'),
    url(r'^$', dashboard, name='dashboard'),
    url(r'^edit/$', edit, name="edit"),
    url(r'^logout/$',  LogoutView.as_view(template_name='student/logged_out.html'), name='logout'),
    url(r'^password-change/$',PasswordChangeViewForStudent.as_view(), name='password_change'),
    url(r'^password-change/done/$',PasswordChangeDoneViewForStudent.as_view(), name='password_change_done'),
    url(r'^', include('assesments.urls', namespace='assesments', app_name='assesments')),
    
    #password reset through email
    url(r'^password_reset/$',StudentPasswordResetView.as_view(),name='password_reset'),
    url(r'^password_reset/done/$',StudentPasswordResetDoneView.as_view(),name='password_reset_done'),
    url(r'^reset/done/$',StudentPasswordResetCompleteView.as_view(),name='password_reset_complete'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        StudentPasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    
    #library 
    url(r'^library-asset/my-issued/$',MyIssuedLibraryAsset.as_view(),name='my_issued_library_asset'),
    url(r'^library-asset/view/$',ViewLibraryAsset.as_view(),name='view_library_asset'),
    
    #result
    url(r'^result/$',StudentResult.as_view(),name='result'),
    url(r'^result/(?P<pk>\d+)/report.pdf/$',ResultReport.as_view(),name='result_report'),
    
    #student registration
    url(r'^registration/$',StudentRegistration.as_view(),name='student_registration'),
]   

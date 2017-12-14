from django.conf.urls import url
from .views import ManageAllAssesmentView, ManageStudentAssesmentView, ProcesStudentAssesmentView




urlpatterns = [
    url(r'^assesment/$', ManageAllAssesmentView.as_view(), name='manage_all_assesment'),
    url(r'^live/$', ManageStudentAssesmentView.as_view(), name='manage_student_assesment'),
    url(r'^process/$', ProcesStudentAssesmentView.as_view(), name='process_assesment'),
   ]

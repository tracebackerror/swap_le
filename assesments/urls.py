from django.conf.urls import url
from .views import ManageAllAssesmentView, ManageStudentAssesmentView, \
 ProcesStudentAssesmentView, assessment_delete_by_staff,  assessment_edit_by_staff, \
 assessment_create_by_staff, ManageSingleAsessment,assessment_question_delete




urlpatterns = [
    url(r'^assesment/$', ManageAllAssesmentView.as_view(), name='manage_all_assesment'),
    url(r'^live/$', ManageStudentAssesmentView.as_view(), name='manage_student_assesment'),
    url(r'^process/$', ProcesStudentAssesmentView.as_view(), name='process_assesment'),
    url(r'^(?P<assesmentid>\w{0,15})/delete/$', assessment_delete_by_staff, name='assessment_delete_by_staff'),
    url(r'^(?P<assesmentid>\w{0,15})/edit/$', assessment_edit_by_staff, name='assessment_edit_by_staff'),
    url(r'^(?P<assesmentid>\w{0,15})/change/$', ManageSingleAsessment.as_view(), name='assessment_manage_by_staff'),
    url(r'^create-assessment/$', assessment_create_by_staff, name='assessment_create_by_staff'),
    url(r'^change/(?P<questionid>\w{0,15})/delete/$', assessment_question_delete, name='assessment_question_delete'),
   ]

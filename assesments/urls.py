from django.conf.urls import url,include
from .views import *
 
from section.views import AddQuestionSection, add_section

app_name='assesments'

urlpatterns = [
    url(r'^assesment/$', ManageAllAssesmentView.as_view(), name='manage_all_assesment'),
    url(r'^live/$', ManageStudentAssesmentView.as_view(), name='manage_student_assesment'),
    url(r'^live/(?P<slug>[\w-]+)$', StartIntroStudentAssesmentView.as_view(), name='student_assesment_intro'),
    
    #url(r'^open/(?P<assesmentid>\w{0,15})/finish/$', GenerateAssesmentResultView.as_view(), name='assesment_open_finished_by_student'),
    #OPEN EXAM
    url(r'^open/$', ManageOpenAssesmentView.as_view(), name='manage_open_assesment'),
    url(r'^open/(?P<slug>[\w-]+)$', OpenIntroStudentAssesmentView.as_view(), name='open_assesment_intro'),
    url(r'^open/process/$', ProcessOpenAssesmentView.as_view(), name='process_open_assesment'),
    url(r'^open/(?P<slug>[\w-]+)/finish/$', GenerateOpenAssesmentResultView.as_view(), name='assesment_open_finished_by_student'),
    url(r'^open/(?P<slug>[\w-]+)/result/(?P<pk>\w{0,15})$', AssessmentOpenResultByStaff.as_view(), name='assessment_open_result_by_staff'),
    
    
    #PUBLIC EXAM
    url(r'^process/$', ProcesStudentAssesmentView.as_view(), name='process_assesment'),
    url(r'^(?P<assesmentid>\w{0,15})/delete/$', assessment_delete_by_staff, name='assessment_delete_by_staff'),
    url(r'^(?P<assesmentid>\w{0,15})/finish/$', GenerateAssesmentResultView.as_view(), name='assesment_finished_by_student'),
    

    url(r'^(?P<assesmentid>\w{0,15})/edit/$', assessment_edit_by_staff, name='assessment_edit_by_staff'),
    url(r'^(?P<assesmentid>\w{0,15})/print/$', assessment_print_by_staff, name='assessment_print_by_staff'),
    url(r'^(?P<assesmentid>\w{0,15})/edit/(?P<questionid>\w{0,15})/delete/$', assessment_question_delete, name='assessment_question_delete'),
    url(r'^result/(?P<pk>\w{0,15})/$', AssessmentResultByStaff.as_view(), name='assessment_result_by_staff'),
    url(r'^(?P<assesmentid>\w{0,15})/change/$', ManageSingleAsessment.as_view(), name='assessment_manage_by_staff'),
    url(r'^create-assessment/$', assessment_create_by_staff, name='assessment_create_by_staff'),
    
    url(r'^change/(?P<questionid>\w{0,15})/edit/$', ManageSingleQuestionUpdateView.as_view(), name='assesment_manage_update_question'),
    url(r'^(?P<assesmentid>\w{0,15})/change/question/add/$', ManageSingleQuestionAddView.as_view(), name='assesment_manage_add_question'),
    url(r'^(?P<assesmentid>\w{0,15})/change/question/clone/(?P<questionid>\w{0,15})$', ManageSingleQuestionAddView.as_view(), name='assesment_manage_add_question_clone'),
    url(r'^(?P<assesmentid>\w{0,15})/change/question/review/$', ReviewAllSqaView.as_view(), name='assesment_manage_review_sqa_question'),
    
    #section
    url(r'^(?P<assesmentid>\w{0,15})/section/add/$',AddQuestionSection.as_view(),name="add_question_section"),
    #url(r'^(?P<assesmentid>\w{0,15})/question-section/add/$',add_section,name="add_question_section"),
    url(r'^section/', include('section.urls', namespace='section', )),
    
    #Result Publish
    url(r'^(?P<assesmentid>\w{0,15})/change/publish-all-results$', PublishAllResults, name='publish_all_results'),
    
    #Tag
    url(
        r'^autocomplete/$',
        TagAutocomplete.as_view(),
        name='tag_autocomplete',
    ),
    
   ]

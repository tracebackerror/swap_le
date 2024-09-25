from django.urls import path, include
from .views import *
from section.views import AddQuestionSection

app_name = 'assesments'

urlpatterns = [
    path('assesment/', ManageAllAssesmentView.as_view(), name='manage_all_assesment'),
    path('live/', ManageStudentAssesmentView.as_view(), name='manage_student_assesment'),
    path('live/<slug:slug>/', StartIntroStudentAssesmentView.as_view(), name='student_assesment_intro'),
    
    # OPEN EXAM
    path('open/', ManageOpenAssesmentView.as_view(), name='manage_open_assesment'),
    path('open/<slug:slug>/', OpenIntroStudentAssesmentView.as_view(), name='open_assesment_intro'),
    path('open/process/', process_open_assessment, name='process_open_assesment'),
    path('open/process2/', process_open_assessment, name='process_new_assesment'),
    path('open/<slug:slug>/finish/', GenerateOpenAssesmentResultView.as_view(), name='assesment_open_finished_by_student'),
    path('open/<slug:slug>/result/<pk>/', AssessmentOpenResultByStaff.as_view(), name='assessment_open_result_by_staff'),
    
    # PUBLIC EXAM
    path('process/', ProcesStudentAssesmentView.as_view(), name='process_assesment'),
    path('<int:assesmentid>/delete/', assessment_delete_by_staff, name='assessment_delete_by_staff'),
    path('<int:assesmentid>/finish/', GenerateAssesmentResultView.as_view(), name='assesment_finished_by_student'),
    path('<int:assesmentid>/edit/', assessment_edit_by_staff, name='assessment_edit_by_staff'),
    path('<int:assesmentid>/print/', assessment_print_by_staff, name='assessment_print_by_staff'),
    path('<int:assesmentid>/print/question/', assessment_print_by_staff_question, name='assessment_print_by_staff_question'),
    path('<int:assesmentid>/edit/<int:questionid>/delete/', assessment_question_delete, name='assessment_question_delete'),
    path('result/<int:pk>/', AssessmentResultByStaff.as_view(), name='assessment_result_by_staff'),
    
    path('questionbank/<int:pk>/', QuestionSet, name="assessment_question_bulk_add"),
    path('<int:assesmentid>/change/', ManageSingleAsessment.as_view(), name='assessment_manage_by_staff'),
    path('create-assessment/', assessment_create_by_staff, name='assessment_create_by_staff'),
    
    path('change/<int:questionid>/edit/', ManageSingleQuestionUpdateView.as_view(), name='assesment_manage_update_question'),
    path('<int:assesmentid>/change/question/add/', ManageSingleQuestionAddView.as_view(), name='assesment_manage_add_question'),
    path('<int:assesmentid>/change/question/clone/<int:questionid>/', ManageSingleQuestionAddView.as_view(), name='assesment_manage_add_question_clone'),
    path('<int:assesmentid>/change/question/review/<int:resultid>/', ReviewAllSqaView.as_view(), name='assesment_manage_review_sqa_question'),
    
    # section
    path('<int:assesmentid>/section/add/', AddQuestionSection.as_view(), name="add_question_section"),
    path('section/', include('section.urls', namespace='section')),
    
    # Result Publish
    path('<int:assesmentid>/change/publish-all-results/', PublishAllResults, name='publish_all_results'),
    path('<int:assesmentid>/change/delete-all-results/', DeleteAllResult, name='assessment_clean_result_by_staff'),
    path('<int:assesmentid>/change/<int:resultid>/delete-single-result/', DeleteSingleResult, name='assessment_result_single_delete'),
    
    # Tag
    path('autocomplete/', TagAutocomplete.as_view(), name='tag_autocomplete'),
]

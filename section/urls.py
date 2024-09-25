from django.urls import path
from .views import *

app_name = 'section'

urlpatterns = [
    path('<int:pk>/delete/', DeleteQuestionSection.as_view(), name="delete_question_section"),
    path('<int:assesmentid>/section/<int:pk>/edit/', EditQuestionSection.as_view(), name="edit_question_section"),
    path('<int:assesmentid>/change/<int:pk>/manage/', ManageQuestionSection.as_view(), name="manage_question_section"),
]

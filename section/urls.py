from django.conf.urls import url
from .views import *

urlpatterns = [
    
    url(r'^(?P<pk>\d+)/delete/$',DeleteQuestionSection.as_view(),name="delete_question_section"),
    url(r'^(?P<pk>\d+)/edit/$',EditQuestionSection.as_view(),name="edit_question_section"),
    url(r'^(?P<pk>\d+)/manage/$',ManageQuestionSection.as_view(),name="manage_question_section"),
    
   ]

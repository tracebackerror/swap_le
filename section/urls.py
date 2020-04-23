from django.conf.urls import url
from .views import *

app_name='section'

urlpatterns = [
    
    url(r'^(?P<pk>\d+)/delete/$',DeleteQuestionSection.as_view(),name="delete_question_section"),
    url(r'^(?P<assesmentid>\w{0,15})/section/(?P<pk>\d+)/edit/$',EditQuestionSection.as_view(),name="edit_question_section"),
    url(r'^(?P<assesmentid>\w{0,15})/change/(?P<pk>\d+)/manage/$',ManageQuestionSection.as_view(),name="manage_question_section"),
    
   ]

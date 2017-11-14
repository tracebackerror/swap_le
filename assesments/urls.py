from django.conf.urls import url
from .views import ManageAllAssesmentView




urlpatterns = [
    url(r'^assesment/$', ManageAllAssesmentView.as_view(), name='manage_all_assesment'),
   ]

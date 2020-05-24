from django.conf.urls import url
from .views import *


app_name='home'

urlpatterns = [
   
    url(r'^google0f6eb0891016c158\.html$', GoogleIndexViewVerification.as_view(), name="googleindexview"),
    
    #url(r'^sw.js', PropellerAds.as_view(), name="propellerads"),
    url(r'^', HomePageView.as_view(), name="homeview"),
    ]
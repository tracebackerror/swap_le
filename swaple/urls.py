from django.conf.urls import url, include
from django.contrib import admin
from home.views import contactus
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap

from assesments.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^institutions/', include('institutions.urls', namespace='institutions', )),
    url(r'^staff/', include('staff.urls', namespace='staff', )),
    url(r'^student/', include('students.urls', namespace='student', )),
    url(r'^', include('home.urls', namespace='home', )),
    url(r'^contactus/',contactus,name='contactus'),
    url(r'^google0f6eb0891016c158\.html$', TemplateView.as_view(template_name='google0f6eb0891016c158.html', content_type='text/plain')), 
    url(r'^tz_detect/', include('tz_detect.urls')),
    
   
   
]

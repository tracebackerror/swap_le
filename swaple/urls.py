from django.conf.urls import url, include
from django.contrib import admin
from home.views import contactus
from django.http import HttpResponse


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^institutions/', include('institutions.urls', namespace='institutions', app_name='institutions')),
    url(r'^staff/', include('staff.urls', namespace='staff', app_name='staff')),
    url(r'^student/', include('students.urls', namespace='student', app_name='student')),
    url(r'^$', include('home.urls', namespace='home', app_name='home')),
    url(r'^contactus/',contactus,name='contactus'),
    url(r'^google0f6eb0891016c158\.html$', lambda r: HttpResponse("google-site-verification: google0f6eb0891016c158.html", mimetype="text/plain")),
    
]

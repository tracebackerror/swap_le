from django.conf.urls import url, include
from django.contrib import admin
from home.views import contactus


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^institutions/', include('institutions.urls', namespace='institutions', app_name='institutions')),
    url(r'^staff/', include('staff.urls', namespace='staff', app_name='staff')),
    url(r'^student/', include('students.urls', namespace='student', app_name='student')),
    url(r'^$', include('home.urls', namespace='home', app_name='home')),
    url(r'^contactus/',contactus,name='contactus')
    
]

from django.urls import path, re_path, include
from django.contrib import admin
from home.views import contactus
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('institutions/', include('institutions.urls', namespace='institutions')),
    path('staff/', include('staff.urls', namespace='staff')),
    path('student/', include('students.urls', namespace='student')),
    path('', include('home.urls', namespace='home')),
    path('contactus/', contactus, name='contactus'),
    re_path(r'^google0f6eb0891016c158\.html$', TemplateView.as_view(template_name='google0f6eb0891016c158.html', content_type='text/plain')),
    path('tz_detect/', include('tz_detect.urls')),
]

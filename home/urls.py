from django.conf.urls import url
from .views import HomePageView, GoogleIndexViewVerification



urlpatterns = [
    url(r'^', HomePageView.as_view(), name="homeview"),
    url(r'^google0f6eb0891016c158.html$', GoogleIndexViewVerification.as_view(), name="googleindexview"),
    ]
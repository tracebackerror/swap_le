from django.conf.urls import url
from .views import *

app_name='fees'

urlpatterns = [
    url(r'^installment/(?P<pk>\d+)/create/$',CreateFeesInstallment.as_view(), name='create_fees_installment'),
    url(r'^installment/(?P<pk>\d+)/manage/$',ManageFeesInstallment.as_view(), name='manage_fees_installment'),
    url(r'^installment/(?P<id>\d+)/manage/(?P<pk>\d+)/edit/$',EditFeesInstallment.as_view(), name='edit_fees_installment'),
    url(r'^installment/(?P<id>\d+)/manage/(?P<pk>\d+)/delete/$',DeleteFeesInstallment.as_view(), name='delete_fees_installment'),
    
]
from django.urls import path
from .views import *

app_name = 'fees'

urlpatterns = [
    path('installment/<int:pk>/create/', CreateFeesInstallment.as_view(), name='create_fees_installment'),
    path('installment/<int:pk>/manage/', ManageFeesInstallment.as_view(), name='manage_fees_installment'),
    path('installment/<int:id>/manage/<int:pk>/edit/', EditFeesInstallment.as_view(), name='edit_fees_installment'),
    path('installment/<int:id>/manage/<int:pk>/delete/', DeleteFeesInstallment.as_view(), name='delete_fees_installment'),
]

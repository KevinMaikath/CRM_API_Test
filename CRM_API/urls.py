from CRM_API.views import CustomerList, CustomerDetail
from django.urls import path

urlpatterns = [
    path('', CustomerList.as_view(), name='customer_list'),
    path('/<int:pk>', CustomerDetail.as_view(), name='customer_detail')
]

from CRM_API.views import CustomerList, CustomerDetail
from django.urls import path

urlpatterns = [
    path('customers', CustomerList.as_view(), name='customer_list'),
    path('customer/<int:pk>', CustomerDetail.as_view(), name='customer_detail')
]

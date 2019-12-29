from django.conf import settings
from django.conf.urls.static import static

from CRM_API.views import CustomerList, CustomerDetail, UserCreate, LoginView
from django.urls import path

urlpatterns = [
    path('customers', CustomerList.as_view(), name='customer_list'),
    path('customer/<int:pk>', CustomerDetail.as_view(), name='customer_detail'),
    path('users', UserCreate.as_view(), name='user_create'),
    path('login', LoginView.as_view(), name='login')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

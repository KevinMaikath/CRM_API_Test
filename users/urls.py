from django.urls import path

from users.views import UserCreate, LoginView

urlpatterns = [
    path('/users', UserCreate.as_view(), name='user_create'),
    path('/login', LoginView.as_view(), name='login')
]

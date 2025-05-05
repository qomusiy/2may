from django.urls import path, include
from .views import RegisterView, Test, LoginView, LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('test/', Test.as_view(), name='test'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
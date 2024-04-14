"""
URL configuration for the User App
"""

from django.urls import path
from .views import RegisterEmailView, RegisterVerifyView, LoginView, RegisterInfoView, LogoutView, GenerateOTPView


app_name = "app.user"

urlpatterns = [
    path("register/", RegisterEmailView.as_view(), name="register-user"),
    path("register/verify/", RegisterVerifyView.as_view(), name="verify-email"),
    path("register/info/", RegisterInfoView.as_view(), name="register-info"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("send-otp/", GenerateOTPView.as_view(), name="send-otp"),
]

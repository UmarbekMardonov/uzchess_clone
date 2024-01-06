from django.urls import path

from authuser import views
from authuser.auth import views as auth
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("token/", TokenObtainPairView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
    path("login/", auth.AuthPhoneAPIView.as_view()),
    path("verify/", auth.AuthVerifyAPIView.as_view()),
    path("register/", auth.AuthPhoneRegisterAPIView.as_view()),
    path("register/verify/", auth.AuthRegisterVerifyAPIView.as_view()),
    path("profile/", views.UserUpdateView.as_view()),
    path("recovery/phone/", views.PhoneRecoveryAPIView.as_view()),
    path("recovery/verify/", views.RecoveryVerifyAPIView.as_view()),
    # EXTRA
    path("users/", views.UserListAPIView.as_view()),
    path("users/<int:pk>/", views.UserDetailView.as_view()),
]

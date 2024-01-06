from rest_framework import generics
from rest_framework.permissions import AllowAny

from authuser import models
from authuser.auth import serializers
# from user.permissions import IsAdmin, IsShopOwner

from rest_framework import generics
from rest_framework.permissions import AllowAny

from authuser import models
from authuser.auth import serializers


class AuthPhoneAPIView(generics.CreateAPIView):
    queryset = models.UserModel.objects.all()
    serializer_class = serializers.AuthPhoneSerializer
    throttle_scope = "auth-sms"
    permission_classes = [AllowAny]


class AuthPhoneRegisterAPIView(generics.CreateAPIView):
    queryset = models.UserModel.objects.all()
    serializer_class = serializers.AuthPhoneRegisterSerializer
    throttle_scope = "auth-sms"
    permission_classes = [AllowAny]


class AuthVerifyAPIView(generics.CreateAPIView):
    queryset = models.UserModel.objects.all()
    serializer_class = serializers.AuthVerifySerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        pass


class AuthRegisterVerifyAPIView(generics.CreateAPIView):
    queryset = models.UserModel.objects.all()
    serializer_class = serializers.AuthRegisterVerifySerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        pass



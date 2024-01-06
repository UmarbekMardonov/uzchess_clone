from django.contrib.auth import get_user_model
from rest_framework import generics, status, views
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
# from authuser.permissions import IsAdmin, IsShopOwner, IsWarehouseOwner, IsSeller
from authuser import models, serializers
from utils.views import FilterByPermission

User = get_user_model()


class UserUpdateView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserShortSerializer
    # permission_classes = (IsAdmin | IsShopOwner,)

    def get_object(self):
        return self.request.user


class ProfileAPIView(generics.RetrieveAPIView):
    serializer_class = serializers.ProfileSerializer
    queryset = User.objects.all()
    lookup_field = "username"


class PhoneRecoveryAPIView(generics.CreateAPIView):
    queryset = models.UserModel.objects.all()
    serializer_class = serializers.PhoneRecoverySerializer
    permission_classes = [AllowAny]


class RecoveryVerifyAPIView(generics.CreateAPIView):
    queryset = models.UserModel.objects.all()
    serializer_class = serializers.RecoveryVerifySerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        pass


class UserListAPIView(generics.ListCreateAPIView):
    queryset = models.UserModel.objects.all()
    serializer_class = serializers.UserSerializers
    # permission_classes = (IsAdmin,)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.UserModel.objects.all()
    serializer_class = serializers.UserSerializers
    # permission_classes = (IsAdmin,)


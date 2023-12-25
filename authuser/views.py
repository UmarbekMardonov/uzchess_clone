from rest_framework import generics
from .serializers import MyTokenObtainPairSerializer, RegisterSerializer, ProfileSerializer, PhoneRecoverySerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import UserModel


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = UserModel.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class UserProfileView(generics.ListAPIView):
    queryset = UserModel.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)
    # search_fields = ('full_name', 'phone_number')


class PhoneRecoveryAPIView(generics.CreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = PhoneRecoverySerializer
    permission_classes = [AllowAny]

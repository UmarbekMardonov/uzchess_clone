from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import MyTokenObtainPairSerializer, RegisterSerializer, ProfileSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import UserProfileModel


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class UserProfileView(generics.ListAPIView):
    queryset = UserProfileModel.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)
    # search_fields = ('full_name', 'phone_number')

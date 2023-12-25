from django.utils import timezone

from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import UserModel, OTP
from django.conf import settings
from course.serializers import CourseBigSerializer
from .validators import phone_number_validators
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = UserModel
        fields = ('full_name', 'phone_number', 'email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = UserModel.objects.create(
            full_name=validated_data['full_name'],
            email=validated_data['email'],
            password=validated_data['password'],
            phone_number=validated_data['phone_number']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class ProfileSerializer(serializers.ModelSerializer):
    course = CourseBigSerializer()

    class Meta:
        model = UserModel
        fields = ['full_name', 'phone_number', 'email', 'course']


class PhoneRecoverySerializer(serializers.Serializer):
    phone_number = serializers.CharField(validators=phone_number_validators)
    active_till = serializers.DateTimeField(read_only=True)
    lifetime = serializers.IntegerField(read_only=True, help_text="OTPcode lifetime seconds")

    def validate(self, attrs):
        if not UserModel.objects.filter(phone_number=attrs["phone_number"]).exists():
            raise serializers.ValidationError("Пользователь с таким номером уже существует")
        return attrs

    def create(self, validated_data):
        phone_number = validated_data["phone_number"]
        now = timezone.now()
        try:
            instance = OTP.objects.filter(active_till__gte=now, receiver=phone_number).last()
            if instance is None:
                raise OTP.DoesNotExist
        except:
            OTP.objects.filter(receiver=phone_number).update(active_till=now)
            instance = OTP.objects.create(
                receiver=phone_number,
                active_till=OTP.otp_lifetime(settings.OTP_EXPIRE_TIME),
            )
        validated_data["active_till"] = instance.active_till
        validated_data["lifetime"] = instance.lifetime
        return validated_data

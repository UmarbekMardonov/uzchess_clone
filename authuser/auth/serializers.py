from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import update_last_login
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from authuser import models
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from django.contrib.auth.hashers import make_password

from authuser.validators import phone_number_validators


class AuthPhoneSerializer(serializers.Serializer):
    phone_number = serializers.CharField(validators=phone_number_validators)
    password = serializers.CharField(
        write_only=True,
    )

    active_till = serializers.DateTimeField(read_only=True)
    lifetime = serializers.IntegerField(read_only=True, help_text="OTPcode lifetime seconds")

    def create(self, validated_data):
        phone_number = validated_data["phone_number"]
        password = validated_data["password"]
        user = authenticate(username=phone_number, password=password)
        if user is None:
            raise AuthenticationFailed("Неверный телефон или пароль")
        now = timezone.now()
        try:
            instance = models.OTP.objects.filter(active_till__gte=now, receiver=phone_number).last()
            if instance is None:
                raise models.OTP.DoesNotExist
        except:
            models.OTP.objects.filter(receiver=phone_number).update(active_till=now)
            instance = models.OTP.objects.create(
                receiver=phone_number,
                active_till=models.OTP.otp_lifetime(settings.OTP_EXPIRE_TIME),
            )
        validated_data["active_till"] = instance.active_till
        validated_data["lifetime"] = instance.lifetime
        return validated_data


class AuthVerifySerializer(serializers.Serializer):
    phone_number = serializers.CharField(validators=phone_number_validators, write_only=True)
    otp_code = serializers.CharField(write_only=True)
    token_class = RefreshToken
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        phone_number = attrs["phone_number"]
        otp_code = attrs["otp_code"]
        instance = self.get_user(otp_code, phone_number)

        refresh = self.get_token(instance)
        attrs["refresh"] = str(refresh)
        attrs["access"] = str(refresh.access_token)
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, instance)
        return attrs

    def get_user(
            self,
            otp_code: str,
            phone_number: str,
    ) -> models.UserModel:
        now = timezone.now()

        try:
            otp = models.OTP.objects.filter(active_till__gte=now, receiver=phone_number).get(
                code=otp_code
            )
            otp.active_till = now
            otp.save(update_fields=["active_till"])

            instance = models.UserModel.objects.get(phone_number=otp.receiver)
            if not instance.is_active:
                instance.save(update_fields=["is_active"])
            return instance
        except models.OTP.DoesNotExist:
            raise ValidationError({"otp_code": _("Invalid code or expired")})

    @classmethod
    def get_token(cls, user):
        return cls.token_class.for_user(user)


class AuthPhoneRegisterSerializer(serializers.Serializer):
    phone_number = serializers.CharField(validators=phone_number_validators)
    active_till = serializers.DateTimeField(read_only=True)
    lifetime = serializers.IntegerField(read_only=True, help_text="OTPcode lifetime seconds")

    def create(self, validated_data):
        phone_number = validated_data["phone_number"]
        if models.UserModel.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError("Пользователь с таким номером уже существует")
        now = timezone.now()
        try:
            instance = models.OTP.objects.filter(active_till__gte=now, receiver=phone_number).last()
            if instance is None:
                raise models.OTP.DoesNotExist
        except:
            models.OTP.objects.filter(receiver=phone_number).update(active_till=now)
            instance = models.OTP.objects.create(
                receiver=phone_number,
                active_till=models.OTP.otp_lifetime(settings.OTP_EXPIRE_TIME),
            )
        validated_data["active_till"] = instance.active_till
        validated_data["lifetime"] = instance.lifetime
        return validated_data


class AuthRegisterVerifySerializer(serializers.Serializer):
    phone_number = serializers.CharField(validators=phone_number_validators, write_only=True)
    password = serializers.CharField(
        write_only=True,
    )
    full_name = serializers.CharField()

    otp_code = serializers.CharField(write_only=True)
    token_class = RefreshToken
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        phone_number = attrs["phone_number"]
        otp_code = attrs["otp_code"]
        instance = self.get_user(otp_code, phone_number, attrs["password"], attrs["full_name"])

        refresh = self.get_token(instance)
        attrs["refresh"] = str(refresh)
        attrs["access"] = str(refresh.access_token)
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, instance)
        return attrs

    def get_user(
            self,
            otp_code: str,
            phone_number: str,
            password: str,
            full_name: str,
    ) -> models.UserModel:
        now = timezone.now()

        try:
            otp = models.OTP.objects.filter(active_till__gte=now, receiver=phone_number).get(
                code=otp_code
            )
            otp.active_till = now
            otp.save(update_fields=["active_till"])

            instance = models.UserModel.objects.create(
                phone_number=phone_number, password=make_password(password), full_name=full_name
            )
            if not instance.is_active:
                instance.save(update_fields=["is_active"])
            return instance
        except models.OTP.DoesNotExist:
            raise ValidationError({"otp_code": _("Invalid code or expired")})

    @classmethod
    def get_token(cls, user):
        return cls.token_class.for_user(user)

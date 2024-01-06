from django.contrib.auth.hashers import make_password
from django.utils import timezone

from rest_framework import serializers
from django.contrib.auth.models import User, update_last_login
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserModel, OTP
from django.conf import settings
from course.serializers import CourseBigSerializer
from .validators import phone_number_validators
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.translation import gettext_lazy as _
from authuser import models


class ShortProfileSerializer(serializers.ModelSerializer):
    """Don't change"""

    class Meta:
        model = User
        fields = "__all__"


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.UserModel
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    blocked_me = serializers.SerializerMethodField()
    in_blacklist = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = "__all__"

    @property
    def user(self):
        return self.context["request"].user

    def get_blocked_me(self, value) -> bool:
        return value.is_blocked_me(self.user.id)

    def get_in_blacklist(self, value) -> bool:
        return self.user.is_blocked_me(value.id)


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("phone_number", "avatar_url", "avatar", "full_name")
        extra_kwargs = {
            "avatar": {"write_only": True},
            "avatar_url": {"read_only": True},
            "phone_number": {"read_only": True},
        }


class TokenObtainPairSerializer(serializers.ModelSerializer):
    token_class = RefreshToken
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    id_token = serializers.CharField(max_length=1024, write_only=True)
    invitation_code = serializers.CharField(
        max_length=10,
        write_only=True,
        default=None,
        required=False,
        allow_null=True,
        allow_blank=True,
    )
    is_new_user = serializers.BooleanField(read_only=True)
    invited = serializers.BooleanField(read_only=True)
    phone_number = serializers.CharField(validators=phone_number_validators)

    class Meta:
        model = User
        fields = [
            "phone_number",
            "id_token",
            "invitation_code",
            "access",
            "refresh",
            "is_new_user",
            "invited",
        ]

    def validate(self, attrs):
        attrs = super().validate(attrs)
        phone_number = attrs["phone_number"]

        instance, is_new_user = self.get_user(phone_number, attrs.pop("invitation_code"))
        refresh = self.get_token(instance)
        attrs["invited"] = getattr(instance, "invited", False)
        attrs["is_new_user"] = is_new_user
        attrs["refresh"] = str(refresh)
        attrs["access"] = str(refresh.access_token)
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, instance)
        return attrs

    def get_user(self, phone_number, invitation_code=None):
        instance, created = User.objects.get_or_create(phone_number=phone_number)

        if created and invitation_code:
            try:
                invitation = User.objects.only("id").get(invitation_code__iexact=invitation_code)
                models.Invitation.objects.create(user_id=invitation.id, friend_id=instance.id)
                instance.invited = True
            except User.DoesNotExist:
                pass

        if instance.is_active:
            return instance, created

        raise ValidationError({"message": _("No active account found with given credentials")})

    @classmethod
    def get_token(cls, user):
        return cls.token_class.for_user(user)


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


class RecoveryVerifySerializer(serializers.Serializer):
    phone_number = serializers.CharField(validators=phone_number_validators, write_only=True)
    otp_code = serializers.CharField(write_only=True)
    password = serializers.CharField(
        write_only=True,
    )

    token_class = RefreshToken
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        phone_number = attrs["phone_number"]
        password = attrs["password"]
        otp_code = attrs["otp_code"]

        instance = self.get_user(otp_code, phone_number)
        instance.password = make_password(password)
        instance.is_active = True
        instance.save(update_fields=["phone_number", "password", "is_active"])
        refresh = self.get_token(instance)
        attrs["invited"] = getattr(instance, "invited", False)
        attrs["refresh"] = str(refresh)
        attrs["access"] = str(refresh.access_token)
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, instance)
        return attrs

    def get_user(
            self,
            otp_code: str,
            phone_number: str,
    ) -> UserModel:
        now = timezone.now()

        try:
            otp = OTP.objects.filter(active_till__gte=now, receiver=phone_number).get(
                code=otp_code
            )
            otp.active_till = now
            otp.save(update_fields=["active_till"])

            instance = User.objects.get(phone_number=phone_number)
            if not instance.is_active:
                instance.save(update_fields=["is_active"])
            return instance
        except OTP.DoesNotExist:
            raise ValidationError({"otp_code": _("Invalid code or expired")})

    @classmethod
    def get_token(cls, user):
        return cls.token_class.for_user(user)

from django.utils import timezone
import random

from django.db import models
from course.models import CourseBig
from django.contrib.auth.models import AbstractUser


class Role(models.TextChoices):
    ADMIN = "ADMIN"


class UserModel(AbstractUser):
    full_name = models.CharField(max_length=220, blank=True, null=True)
    phone_number = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField()
    date_joined = models.DateTimeField(auto_now_add=True)
    course = models.ManyToManyField(CourseBig, blank=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    user_permissions = None
    # role = models.CharField(choices=Role.choices, max_length=220, default=Role.)
    first_name = None
    last_name = None
    is_staff = None
    groups = None
    username = None
    last_login = None

    def __str__(self):
        return self.full_name


class OTP(models.Model):
    """one-time password"""

    receiver = models.CharField(max_length=32)
    code = models.CharField(max_length=64)
    active_till = models.DateTimeField(editable=False)

    def get_new_code(self):
        code = random.randint(100000, 999999)
        while OTP.objects.filter(code=code, active_till__gte=timezone.now()).exists():
            code = random.randint(100000, 999999)
        return code

    @property
    def lifetime(self) -> int:
        x = self.active_till - timezone.now()
        return x.seconds

    @classmethod
    def otp_lifetime(cls, minutes: int = 60):
        return timezone.now() + timezone.timedelta(minutes=minutes)

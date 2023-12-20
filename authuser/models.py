from django.db import models
from course.models import CourseBig
from django.contrib.auth.models import AbstractUser


class UserModel(AbstractUser):
    full_name = models.CharField(max_length=220, blank=True, null=True)
    phone_number = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField()
    date_joined = models.DateTimeField(auto_now_add=True)
    first_name = None
    last_name = None
    is_staff = None
    is_active = None
    groups = None
    user_permissions = None
    username = None
    last_login = None

    def __str__(self):
        return self.full_name


class UserProfileModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    course = models.ManyToManyField(CourseBig)

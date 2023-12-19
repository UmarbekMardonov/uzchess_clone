from django.db import models
from django.contrib.auth.models import User
from course.models import CourseBig


class ProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=220)
    tel_number = models.CharField(max_length=220)
    email = models.EmailField(blank=True, null=True)
    course = models.ForeignKey(CourseBig, on_delete=models.CASCADE, blank=True, null=True)


    def __str__(self):
        return self.user

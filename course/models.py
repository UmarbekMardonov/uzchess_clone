from django.contrib.auth.models import User
from django.db import models
from django.db.models import ForeignKey


class Level(models.Choices):
    beginner = 'Beginner'
    intermediate = 'Intermediate'
    professional = 'Professional'


class Mentor(models.Model):
    full_name = models.CharField(max_length=220)
    # email = models.EmailField()
    # phone_number = models.CharField(max_length=220)
    description = models.TextField()

    def __str__(self):
        return self.full_name


class CourseBig(models.Model):
    title = models.CharField(max_length=220, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    rating = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='User', blank=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    level = models.CharField(max_length=220, choices=Level.choices, blank=True, null=True)

    def __str__(self):
        return self.title


class CourseLittle1(models.Model):
    title = models.CharField(max_length=220)
    course_big = models.ForeignKey(CourseBig, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class CourseLittle2(models.Model):
    title = models.CharField(max_length=220)
    mentor = ForeignKey(Mentor, on_delete=models.CASCADE)
    course_little_1 = models.ForeignKey(CourseLittle1, on_delete=models.CASCADE)
    description = models.TextField()
    video = models.FileField(upload_to='videos/', blank=True, null=True)

    def __str__(self):
        return self.title
# class Complaint(models.Choices):
#     zoravonlik
#

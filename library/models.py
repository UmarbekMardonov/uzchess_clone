from django.contrib.auth.models import User
from django.db import models
from course.serializers import Level


class Book(models.Model):
    title = models.CharField(max_length=220)
    author = models.CharField(max_length=220)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    level = models.CharField(max_length=220, choices=Level.choices, blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    rating = models.DecimalField(max_digits=10, decimal_places=1, blank=True, null=True)
    pages_count = models.IntegerField(default=0)
    description = models.TextField()
    wrote_date = models.IntegerField()

    def __str__(self):
        return self.title

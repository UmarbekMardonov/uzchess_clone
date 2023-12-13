from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=220)
    mentor = models.CharField(max_length=220)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10)
    like = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=10, decimal_places=1)
    

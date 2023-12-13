from django.db import models


class News(models.Model):
    title = models.CharField(max_length=220)
    description1 = models.TextField()
    image = models.ImageField(upload_to='images/')
    description2 = models.TextField()
    views = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

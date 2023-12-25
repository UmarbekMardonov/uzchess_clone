from django.db import models
from ckeditor.fields import RichTextField


class News(models.Model):
    content = RichTextField(blank=True, null=True)
    title = models.CharField(max_length=220)
    image = models.ImageField(upload_to='images/')
    views = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'

    def __str__(self):
        return self.title



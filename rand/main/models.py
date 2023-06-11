from django.db import models
from django.contrib.auth.models import User



class Topics(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    link = models.URLField(max_length=200, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    date_watched = models.DateTimeField(auto_now=True, blank=True)
    is_watched = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'topic'
        verbose_name_plural = 'topics'

    def __str__(self):
        if self.subtitle:
            return f'{self.title} / {self.subtitle}'
        return f'{self.title}'

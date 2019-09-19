from django.conf import settings
from django.db import models
from django.utils import timezone


class Score(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.TextField()

# Create your models here.

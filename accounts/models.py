from django.conf import settings
from django.db import models
from django.utils import timezone


class Score(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    scoreModule1 = models.IntegerField()
    scoreModule2 = models.IntegerField()
    scoreModule3 = models.IntegerField()
    scoreModule4 = models.IntegerField()
    scoreModule5 = models.IntegerField()
    scoreModule6 = models.IntegerField()
    scoreModule7 = models.IntegerField()
    scoreModule8 = models.IntegerField()
    scoreModule9 = models.IntegerField()
    scoreModule10 = models.IntegerField()
    scoreModule11 = models.IntegerField()
    scoreModule12 = models.IntegerField()
    scoreModule13 = models.IntegerField()
    scoreModule14 = models.IntegerField()
    scoreModule15 = models.IntegerField()
    scoreModule16 = models.IntegerField()
    scoreModule17 = models.IntegerField()
    scoreModule18 = models.IntegerField()
    scoreModule19 = models.IntegerField()
    scoreModule20 = models.IntegerField()

# Create your models here.

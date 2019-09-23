from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.

class User(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    generalIntelligence = models.IntegerField(default = 0)

class Module(models.Model):
    moduleName = models.CharField(max_length=42)
    

class Module_User(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    currentModule = models.BooleanField(default = False)
    amountCorrect = models.IntegerField(default = 0)
    amountWrong = models.IntegerField(default = 0)
    amountHints = models.IntegerField(default = 0)
    moduleScore = models.IntegerField(default = 0)

class Chapter(models.Model):
    chapterName = models.CharField(max_length=42)

class Chapter_User(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    chapterIntelligence = models.IntegerField(default = 0)
    



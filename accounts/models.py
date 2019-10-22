from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser



# Create your models here.

class CustomUser(AbstractUser):
    generalIntelligence = models.IntegerField(default = 0)
    name = models.CharField(max_length=42)
    isTeacher = models.BooleanField(default = False)
    
    def __str__(self):
        return self.email
        

class Module(models.Model): 
    title = models.CharField(max_length=200)
    text = models.TextField()
    
    def publish(self):
        self.publish_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def template_name(self):
        return self
        # return str self.title .html str make this a combination of a string with the title-variable and '.html' !

    # has sub-modules
    # has Module Exam

class Module_User(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    currentModule = models.IntegerField(default = 0)
    amountCorrect = models.IntegerField(default = 0)
    amountWrong = models.IntegerField(default = 0)
    amountHints = models.IntegerField(default = 0)
    moduleScore = models.IntegerField(default = 0)
    mistake1 = models.IntegerField(default = 0)
    mistake2 = models.IntegerField(default = 0)
    mistake3 = models.IntegerField(default = 0)
    mistake4 = models.IntegerField(default = 0)
    mistake5 = models.IntegerField(default = 0)
    currentQuestionHints = models.IntegerField(default = 0)
    currentQuestionCorrect = models.IntegerField(default = 0)

class Chapter(models.Model):
    name = models.CharField(max_length=200)

class Chapter_User(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    chapterIntelligence = models.IntegerField(default = 0)
    
class ModuleOverview(models.Model): 
    title = models.CharField(max_length=200)
    text = models.TextField()
    
    def publish(self):
        self.publish_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class SubModule(models.Model): # make a child of Module?
    title = models.CharField(max_length=200)
    text = models.TextField()
    
    def publish(self):
        self.publish_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def template_name(self):
        return self
        # return str self.title .html str make this a combination of a string with the title-variable and '.html' !

    # has exercises

class Exercise(models.Model): # make a child of Sub-Module?
    title = models.CharField(max_length=200)
    text = models.TextField()
    
    def publish(self):
        self.publish_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def template_name(self):
        return self
        # return str self.title .html str make this a combination of a string with the title-variable and '.html' !

    # make children for the various types of exercises
     
class Exam(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    
    def publish(self):
        self.publish_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def template_name(self):
        return self
        # return str self.title .html str make this a combination of a string with the title-variable and '.html' !

    # select exercises from each submodule for a module, and from each module for 'overview-tests'

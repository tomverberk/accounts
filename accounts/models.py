from django.conf import settings
from django.db import models
from django.utils import timezone


class Score(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.TextField()

class ModuleOverview(models.Model): 
    title = models.CharField(max_length=200)
    text = models.TextField()
    
    def publish(self):
        self.publish_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

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

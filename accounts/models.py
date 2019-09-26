from django.conf import settings
from django.db import models
from django.utils import timezone


class Score(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.TextField()

class ModuleOverview(models.Model): 
    def __init__(self, name):
        self.name = 'moduleOverview'
    
    title = models.CharField(max_length=200)
    text = models.TextField()
    # submodule = models.SubModule()
    # module_exam = models.ModuleExam()

#class Module():
#    def __init__(self,name,subs):
#        self.name = moduleName
#        self.subs = 5
    # template for specific module
    # url for specific module

    # has subModules

# class SubModule():
#    def __init__(self, name, exercises):
#        self.name = subModuleName
        # self.name = moduleName.SubNumber     ## this is the format that is preferable
    
    # template for specific submodule
    # url for specific submodule

    # has Exercises 

#class Exercise():
#    def __init__(self, name):
#        self.name = Exercise

#class Exam():

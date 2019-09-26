# accounts/views.py
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render
from .models import Score

def showInfo(request):
    score = Score.objects.all()
    return render(request, 'accounts/showInfo.html', {'score': score})

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

# def ModuleOverview(request):
#   overview = ModuleOverview.text()
#   return render(request, 'moduleOverview.html', {'Module Overzicht': overview} )

class ModuleOverview():
    template_name = 'moduleOverview.html'

class Module1():
    template_name = 'module1.html'

class Module1_1():
    template_name = 'module1_1.html'

class Module1_2():
    template_name = 'module1_2.html'

class Module1_3():
    template_name = 'module1_3.html'

class Module1_4():
    template_name = 'module1_4.html'

class Module1_5():
    template_name = 'module1_5.html'

class Module1_6():
    template_name = 'module1_6.html'

class Module1_exam():
    template_name = 'module1_exam.html'

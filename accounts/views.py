# accounts/views.py
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render
from django.http import HttpResponse
from .models import Score, ModuleOverview, Module, SubModule, Exam

def showInfo(request):
    score = Score.objects.all()
    return render(request, 'accounts/showInfo.html', {'score': score})

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

def moduleOverview(request):     # maybe make this a normal class as well, and just fill the few submodules manually?
   list = ModuleOverview.text
   return render(request, 'moduleOverview.html', {'Hoofdstukken overzicht': list} )

def module1(request):
    text = "Wat is het goede antwoord " # % number
    return render(request,'module1.html', {'vraag': text} )
    #return render(request, 'accounts/module1_1.html', {'vragen lijst': text} )

def module1_1(request):
    text = "Wat is het goede antwoord " # % number
    return render(request,'module1_1.html', {'vraag': text} )

def module1_2(request):
    text = "Wat is het goede antwoord " # % number
    return render(request,'module1_1.html', {'vraag': text} )

def module1_3(request):
    text = "Wat is het goede antwoord " # % number
    return render(request,'module1_1.html', {'vraag': text} )

def module1_4(request):
    text = "Wat is het goede antwoord " # % number
    return render(request,'module1_1.html', {'vraag': text} )

def module1_5(request):
    text = "Wat is het goede antwoord " # % number
    return render(request,'module1_1.html', {'vraag': text} )

def module1_exam(request):
    text = "Wat is het goede antwoord " # % number
    return render(request,'module1_exam.html', {'vraag': text} )
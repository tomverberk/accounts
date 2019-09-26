# accounts/views.py
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render
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

moduleone = Module()
moduleone.template_name = 'module1.html'

module1_1 = SubModule()
module1_1.template_name = 'module1.html'

module1_2 = SubModule()
module1_2.template_name = 'module1_2.html'

module1_3 = SubModule()
module1_3.template_name = 'module1_3.html'

module1_4 = SubModule()
module1_4.template_name = 'module1_4.html'

module1_5 = SubModule()
module1_5.template_name = 'module1_5.html'

module1_exam = Exam()
module1_exam.template_name = 'module1_exam.html'
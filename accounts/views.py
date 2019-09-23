# accounts/views.py
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render
from .models import User

def showInfo(request):
    generateIntelligence = generateIntelligence.objects.all()
    return render(request, 'accounts/showInfo.html', {'generalIntelligence': generalIntelligence})

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
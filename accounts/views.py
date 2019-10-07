# accounts/views.py
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render
from django.http import HttpResponse
from .models import User, ModuleOverview, Module, SubModule, Exam
from .forms import AnswerForm
import random
#import numpy as np


def showInfo(request):
#    generateIntelligence = generateIntelligence.objects.all()
    return render(request, 'accounts/showInfo.html' ) #{'generalIntelligence': generalIntelligence})

def exampleQuestion(request):
    question = {}
    a = random.randint(1,101)
    b = random.randint(1,101)
    question["question"] = "%s + %s =" %(a,b)  
    question["answer"] = "%s" %(a+b)
    global correct_answer
    correct_answer = question["answer"]
    questions = []
    questions.append(question)
    
    return render(request, 'accounts/exampleQuestion.html', {'questions':questions})

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

def moduleOverview(request):     # maybe make this a normal class as well, and just fill the few submodules manually?
   list = ModuleOverview.text
   return render(request, 'moduleOverview.html', {'Hoofdstukken overzicht': list} )

def module1(request):
    text = "Wat is het goede antwoord " # % number
    return render(request,'module1/module1.html', {'vraag': text} )
    #return render(request, 'accounts/module1_1.html', {'vragen lijst': text} )

def module1_1(request):
    text = "Wat is het goede antwoord " # % number
    return render(request,'module1/module1_1.html', {'vraag': text} )

def module1_1a(request):
    question = {}
    a = random.randint(-20,20)
    b = random.randint(-20,20)
    c = random.randint(-20,20)
    d = random.randint(-3,3)
    question["question"] = "%sx + %s + %sx + %s" %(a,b,c,d)  #vary which terms have 'x'? # vary name 'x', # +- = -
    question["answer_1"] = "%s" %(a+c)
    question["answer_2"] = "%s"  %(b+d) 
    question["answer"] = question["answer_1"], question["answer_2"]
    global correct_answer
    correct_answer = question["answer"]
    questions = []
    questions.append(question)
    
    return render(request, 'module1/module1_1a.html', {'questions':questions})

def answer1_1a(request):
    #global answer
    answerGiven = request.POST['answer_1'], request.POST['answer_2']
    answerOriginal = correct_answer
    if answerGiven == answerOriginal:
        text = "Jouw antwoord was goed!"
    else:
        text = "Jouw antwoord was fout."
    
    return render(request, 'accounts/answers/answer1_1a.html', {'answerGiven_1':answerGiven[0],'answerGiven_2':answerGiven[1], \
        'answerOriginal_1':answerOriginal[0], 'answerOriginal_2':answerOriginal[1],'text': text})

def module1_1b(request):
    question = {}
    a = random.randint(-10,10)
    b = random.randint(-20,20)
    c = random.randint(-20,20)
    d = random.randint(-5,5)
    question["question"] = "%sx + %s = %sx + %s" %(a,b,c,d)  #vary which terms have 'x'? # vary name 'x', # +- = -
    question["answer_1"] = "%s" %(a-c)
    question["answer_2"] = "%s" %(d-b) 
    question["answer"] = question["answer_1"], question["answer_2"]
    global correct_answer
    correct_answer = question["answer"]
    questions = []
    questions.append(question)
    
    return render(request, 'module1/module1_1b.html', {'questions':questions})

def answer1_1b(request):
    #global answer
    answerGiven = request.POST['answer_1'], request.POST['answer_2']
    answerOriginal = correct_answer
    if answerGiven == answerOriginal:
        text = "Jouw antwoord was goed!"
    else:
        text = "Jouw antwoord was fout."
    
    return render(request, 'accounts/answers/answer1_1b.html', {'answerGiven_1':answerGiven[0],'answerGiven_2':answerGiven[1], \
        'answerOriginal_1':answerOriginal[0], 'answerOriginal_2':answerOriginal[1],'text': text})

def module1_1c(request):
    question = {}
    question["answer"] = random.randint(-20,20)
    if question["answer"]==0:
        question["answer"] = 1
    left = random.randint(-10,10)
    right = left*question["answer"]
    c = random.randint(-20,20)
    a = left + c
    b = random.randint(-20,20)
    d = right + b
    question["question"] = "%sy + %s = %sy + %s" %(a,b,c,d)  #vary which terms have 'x'? # vary name 'x', # +- = -
    question["answer_1"] = a - c
    question["answer_2"] = d - b
    global correct_answer
    correct_answer = question["answer"]
    questions = []
    questions.append(question)
    
    return render(request, 'module1/module1_1c.html', {'questions':questions})

def answer1_1c(request):
    #global answer
    answerGiven = request.POST['answer_1']
    answerOriginal = correct_answer
    if answerGiven == answerOriginal:
        text = "Jouw antwoord was goed!"
    else:
        text = "Jouw antwoord was fout."
    
    return render(request, 'accounts/answers/answer1_1c.html', {'answerGiven':answerGiven, 'answerOriginal':answerOriginal, 'text': text})

def module1_2(request):
    text = "Wat is het goede antwoord " # % number
    return render(request,'module1/module1_1.html', {'vraag': text} )

def module1_3(request):
    text = "Wat is het goede antwoord " # % number
    return render(request,'module1/module1_1.html', {'vraag': text} )

def module1_4(request):
    text = "Wat is het goede antwoord " # % number
    return render(request,'module1/module1_1.html', {'vraag': text} )

def module1_5(request):
    text = "Wat is het goede antwoord " # % number
    return render(request,'module1/module1_1.html', {'vraag': text} )

def module1_exam(request):
    text = "Wat is het goede antwoord " # % number
    return render(request,'module1/module1_exam.html', {'vraag': text} )



def get_answer(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AnswerForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:


            return HttpResponse('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AnswerForm()

    return render(request, 'exampleQuestion.html', {'form': form})

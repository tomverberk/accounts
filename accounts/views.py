# accounts/views.py
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render
from django.http import HttpResponse
from .models import User, Score, ModuleOverview, Module, SubModule, Exam
from .forms import AnswerForm
import random


def showInfo(request):
    generateIntelligence = generateIntelligence.objects.all()
    return render(request, 'accounts/showInfo.html', {'generalIntelligence': generalIntelligence})

def exampleQuestion(request):
    question = {}
    a = random.randint(1,101)
    b = random.randint(1,101)
    question["question"] = "%s + %s =" %(a,b)  
    question["answer"] = "%s" %(a+b)
    global answer
    answer = question["answer"]
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
def answer(request):
    global answer
    answerGiven = request.POST['answer']
    answerOriginal = answer
    print(answerGiven)
    print(answer)
    print(answerOriginal)
    if answerGiven == answerOriginal:
        text = "your answer was correct"
    else:
        text = "your answer was wrong"
    
    return render(request, 'accounts/answer.html', {'answerGiven':answerGiven, 'answerOriginal':answerOriginal, 'text': text})

    

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


            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AnswerForm()

    return render(request, 'exampleQuestion.html', {'form': form})

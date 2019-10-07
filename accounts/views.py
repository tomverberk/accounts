# accounts/views.py
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render
from django.http import HttpResponse
from .models import CustomUser, ModuleOverview, Module, SubModule, Exam
from .forms import AnswerForm
import random
import mysql.connector
from mysql.connector import MySQLConnection, Error
from .forms import CustomUserCreationForm, CustomUserChangeForm
import sqlite3
from sqlite3 import Error
import getpass


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
 
    return conn

def create_user(conn, user):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = """INSERT INTO accounts_module_user (user_id, currentModule, amountCorrect, amountWrong, amountHints, moduleScore, module_id, mistake1, mistake2, mistake3, mistake4, mistake5, currentQuestionHints, currentQuestionCorrect) 
                                VALUES (?, false, 0, 0, 0, 0, ?, 0, 0, 0, 0, 0, 0, 0) """
    cur = conn.cursor()
    cur.execute(sql, user)
    return cur.lastrowid

def insertNewUser(user_id):
    database = r"C:/Users/s162449/Documents/Uni/year-4/quartile-1/0LAUK0-Robots-everywhere/accounts-Github/accounts/db.sqlite3"
 
    # create a database connection
    conn = create_connection(database)
    print('ahhhhh')

    modules = Module.objects.all()
    for module in modules:
        with conn:
            # create a new project
            user_Module = (user_id, module.id);
            addModule = create_user(conn, user_Module)

def AnswerAnswered(user_id, module_id, correct, hintsUsed):
    database = r"C:/Users/s162449/Documents/Uni/year-4/quartile-1/0LAUK0-Robots-everywhere/accounts-Github/accounts/db.sqlite3"
 
    # create a database connection
    conn = create_connection(database)

    with conn:
        # create a new project
            answerAnsweredDatabase(conn, user_id, module_id, correct, hintsUsed)


def answerAnsweredDatabase(conn, user_id, module_id, correct, hintsUsed):
    user_module = (user_id, module_id)
    if correct:
        sql_request_amount = 'SELECT amountCorrect, amountHints, currentQuestionHints, currentQuestionCorrect FROM accounts_module_user WHERE user_id = ? AND module_id = ?'
    else:
        sql_request_amount = 'SELECT amountWrong, amountHints, currentQuestionHints, currentQuestionCorrect FROM accounts_module_user WHERE user_id = ? AND module_id = ?'


    cur = conn.cursor()
    cur.execute(sql_request_amount, user_module)
    records = cur.fetchall()
    if(correct):
        newCurrentQuestionCorrect = records[0][3]+1
    else:
        newCurrentQuestionCorrect = records[0][3]
    newAmountHints = records[0][1]+hintsUsed
    newcurrentQuestionHints = records[0][2]+hintsUsed
    newAmountCorrect_Wrong = records[0][0]+1
    newcorrect = [newAmountCorrect_Wrong, newAmountHints, newcurrentQuestionHints, newCurrentQuestionCorrect, user_id, module_id]

    if correct:
        sql = 'UPDATE accounts_module_user SET amountCorrect = ?, amountHints = ?, currentQuestionHints = ?, currentQuestionCorrect = ? WHERE user_id = ? AND module_id = ?'
    else:
        sql = 'UPDATE accounts_module_user SET amountWrong = ?, amountHints = ?, currentQuestionHints = ?, currentQuestionCorrect = ? WHERE user_id = ? AND module_id = ?'

    cur = conn.cursor()
    cur.execute(sql,newcorrect)

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

def signUp(request):
    
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            
            users = CustomUser.objects.all()
            for user in users:
                if user.username == username:
                    insertNewUser(user.id)
                    request.session['username'] = user.id

            return render(request, 'home.html')
    else:
        form_class = CustomUserCreationForm
        success_url = reverse_lazy('login')
        template_name = 'signup.html'
        form = CustomUserCreationForm(request.POST)
    return render(request, 'signup.html', {'form': form})
    


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
    answerOriginal = correct_answer
    print(answerGiven)
    print(correct_answer)
    print(answerOriginal)
    user = request.user
    module_id = 1
    
    if answerGiven == answerOriginal:
        text = "your answer was correct"
        AnswerAnswered(user.id, module_id, True, 0)

    else:
        text = "your answer was wrong"
        AnswerAnswered(user.id, module_id, False, 0)
    
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


            return HttpResponse('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AnswerForm()

    return render(request, 'exampleQuestion.html', {'form': form})

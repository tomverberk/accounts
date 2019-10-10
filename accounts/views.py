# accounts/views.py
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render
from django.http import HttpResponse
from .models import CustomUser, ModuleOverview, Module, SubModule, Exam
from .forms import AnswerForm, CustomUserCreationForm, CustomUserChangeForm
import random, sqlite3, getpass
from sqlite3 import Error
#import numpy as np

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
    database = r"C:/MathApp/accounts/db.sqlite3"
    #database = r"C:/Users/s162449/Documents/Uni/year-4/quartile-1/0LAUK0-Robots-everywhere/accounts-Github/accounts/db.sqlite3"

    # create a database connection
    conn = create_connection(database)
    print('ahhhhh')

    modules = Module.objects.all()
    for module in modules:
        with conn:
            # create a new project
            user_Module = (user_id, module.id)
            addModule = create_user(conn, user_Module)
 
def AnswerAnswered(user_id, module_id, correct, hintsUsed):
    #database = r"C:/Users/s162449/Documents/Uni/year-4/quartile-1/0LAUK0-Robots-everywhere/accounts-Github/accounts/db.sqlite3"
    database = r"C:/MathApp/accounts/db.sqlite3"
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
    question["answer"] = 4 # random.randint(-20,20)
    if  question["answer"]==0:
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
    correct_answer = str(question["answer"])
    questions = []
    questions.append(question)

    return render(request, 'module1/module1_1c.html', {'questions':questions})

def answer1_1c(request):
    global answer
    answerGiven = request.POST['answer']
    answerOriginal = correct_answer
    answerDiv = str(round(1/float(answerOriginal),2))
    if answerGiven == answerDiv:
       text = "Jouw antwoord was fout. Hint: Let op met delen."
    elif answerGiven == answerOriginal:
       text = "Jouw antwoord was goed!"
    else:
       text = "Jouw antwoord was fout. Let goed op de plus- en mintekens."
    
    return render(request, 'accounts/answers/answer1_1c.html', {'answerGiven':answerGiven, 'answerOriginal':answerOriginal,'answerDiv':answerDiv, 'text': text})

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

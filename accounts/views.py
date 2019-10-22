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
    global variables
    variables = [a,b,c,d]
    question["question"] = "%sx + %s + %sx + %s" %(a,b,c,d) 
    question["answer_1"] = "%s" %(a+c)
    question["answer_2"] = "%s" %(b+d)
    question["answer"] = question["answer_1"], question["answer_2"]
    global correct_answer
    correct_answer = question["answer"]
    questions = []
    questions.append(question)

    return render(request, 'module1/module1_1a.html', {'questions':questions})

def answer1_1a(request):
    question = "%sx + %s + %sx + %s" %(variables[0],variables[1],variables[2],variables[3])
    answerGiven = request.POST['answer_1'], request.POST['answer_2']
    answerOriginal = correct_answer
    if answerGiven[0] != answerOriginal[0] and answerGiven[1] != answerOriginal[1]:
        text = "Jouw antwoord was fout."
        hint = "De x-termen én constanten zijn niet goed bij elkaar opgeteld."
    elif  answerGiven[0] != answerOriginal[0]:
        text = "Jouw antwoord was fout."
        hint = "De x-termen zijn niet goed opgeteld."
    elif answerGiven[1] != answerOriginal[1]:
        text = "Jouw antwoord was fout."
        hint = "De constanten zijn niet goed opgeteld."
    elif answerGiven == - answerOriginal:
        text = "Jouw antwoord was fout."
        hint = "Let op met plus- en mintekens wegstrepen."
    elif answerGiven == answerOriginal:
        text = "Jouw antwoord was goed!"
        hint = "Doe de vraag nog een keer, of ga naar de volgende vraag."
    else:
        text = "Jouw antwoord was fout."
        hint = "Let goed op de plus- en mintekens."
    
    return render(request, 'accounts/answers/answer1_1a.html', {'answerGiven_1':answerGiven[0],'answerGiven_2':answerGiven[1], \
        'answerOriginal_1':answerOriginal[0], 'answerOriginal_2':answerOriginal[1],'text': text, 'hint': hint, 'question': question})

def module1_1b(request):
    question = {}
    a = random.randint(-10,10)
    b = random.randint(-20,20)
    c = random.randint(-20,20)
    d = random.randint(-5,5)
    global variables
    variables = [a,b,c,d]
    question["question"] = "%sx + %s = %sx + %s" %(a,b,c,d)  
    question["answer_1"] = "%s" %(a-c)
    question["answer_2"] = "%s" %(d-b)
    question["answer"] = question["answer_1"], question["answer_2"]
    global correct_answer
    correct_answer = question["answer"]
    questions = []
    questions.append(question)

    return render(request, 'module1/module1_1b.html', {'questions':questions})

def answer1_1b(request):
    question = "%sx + %s = %sx + %s" %(variables[0],variables[1],variables[2],variables[3])
    answerGiven = request.POST['answer_1'], request.POST['answer_2']
    answerOriginal = correct_answer
    if answerGiven[0] != answerOriginal[0] and answerGiven[1] != answerOriginal[1]:
        text = "Jouw antwoord was fout."
        hint = "Tel de x-termen goed op aan de linkerzijde. Tel de constanten goed op aan de rechterzijde. Let goed op plus- en mintekens."
    elif answerGiven[0] != answerOriginal[0]:
        text = "Jouw antwoord was fout."
        hint = "De linkerzijde heeft niet (alleen) het goede aantal x-termen. Let goed op plus- en mintekens."
    elif answerGiven[1] != answerOriginal[1]:
        text = "Jouw antwoord was fout."
        hint =  "De rechterzijde heeft niet de goede waarde, de constanten zijn niet goed opgeteld. Let goed op plus- en mintekens."
    elif answerGiven == - answerOriginal:
        text = "Jouw antwoord was fout."
        hint = "Let op met plus- en mintekens wegstrepen."
    elif answerGiven == answerOriginal:
        text = "Jouw antwoord was goed!"
        hint = "Doe de vraag nog een keer, of ga naar de volgende vraag."
    else:
        text = "Jouw antwoord was fout."
        hint = "Let goed op de plus- en mintekens."

    return render(request, 'accounts/answers/answer1_1b.html', {'answerGiven_1':answerGiven[0],'answerGiven_2':answerGiven[1], \
        'answerOriginal_1':answerOriginal[0], 'answerOriginal_2':answerOriginal[1],'text': text, 'hint': hint, 'question': question})

def module1_1c(request):
    question = {}
    question["answer"] = random.randint(-20,20)
    if  question["answer"]==0:
        question["answer"] = 1
    left = random.randint(-10,10)
    if  left==0:
        left = 1
    right = left*question["answer"]
    c = random.randint(-20,20)
    a = left + c
    b = random.randint(-20,20)
    d = right + b
    global variables
    variables = [a,b,c,d]
    question["question"] = "%sy + %s = %sy + %s" %(a,b,c,d)
    question["answer_1"] = a - c
    question["answer_2"] = d - b
    global correct_answer
    correct_answer = question["answer"]
    questions = []
    questions.append(question)

    return render(request, 'module1/module1_1c.html', {'questions':questions})

def answer1_1c(request):
    question = "%sy + %s = %sy + %s" %(variables[0],variables[1],variables[2],variables[3])
    answerGiven = float(request.POST['answer'])
    answerOriginal = float(correct_answer)
    answerDiv = round(1/answerOriginal,2)
    if answerGiven == answerOriginal:
        text = "Jouw antwoord was goed!"
        hint = "Doe de vraag nog een keer, of ga naar de volgende vraag."
    elif answerGiven == - answerOriginal:
        text = "Jouw antwoord was fout."
        hint = "Let op met plus- en mintekens wegstrepen."
    elif answerGiven == answerDiv:
        text = "Jouw antwoord was fout."
        hint = "Let op met delen."
    elif answerGiven == float(round(( variables[3] + variables[1] )/ (variables[0] + variables[2] ), 2)):
        text = "Jouw antwoord was fout."
        hint = "Let goed op plus- en mintekens bij het omzetten van beide termen."
    elif answerGiven == float(round((  variables[3] + variables[1] )/ (variables[0] - variables[2] ),2)):
        text = "Jouw antwoord was fout."
        hint = "Let goed op met het optellen of aftrekken van de constanten."
    elif answerGiven == float(round(( variables[3] - variables[1] )/ (variables[0] + variables[2] ), 2)):
        text = "Jouw antwoord was fout."
        hint = "Let goed op met het optellen of aftrekken van de x-termen."
    else:
       text = "Jouw antwoord was fout." 
       hint = "Let goed op de plus- en mintekens."
    
    return render(request, 'accounts/answers/answer1_1c.html', {'answerGiven':answerGiven, 'answerOriginal':answerOriginal, \
        'text': text, 'hint': hint, 'question': question})

def module1_1d(request):
    question = {}
    question["answer"] = random.randint(-10,10)
    if  question["answer"]==0:
        question["answer"] = 1
    bottom = random.randint(-10,10)
    if  bottom== 0:
         bottom = 1
    top = bottom*question["answer"]

    #b,e,h,k : a + (bx+c). 
    b = 1 #minus values cause a problem here..., prevents divide by zero for a (see below)
    e = random.randint(-13,13)
    h = random.randint(-5,5)
    k = random.randint(-3,3)

    #a,d,g,j: constants before brackets, solves with bottom 
    g = 1 #minus values cause a problem here,  prevents divide by zero for i (see below)
    d = random.randint(-5,5) 
    j =  random.randint(-5,5)
    a = (bottom - d*e + g*h + j*k)/b
    if a == 0: #make sure solving is also carried through to 'top'-solve
        d = d + 1
        e = e + 2
        h = h + 5
        a = (bottom - d*e + g*h + j*k)/b
    question["answer_bottom"] = a*b + d*e - g*h - j*k
    
    #c,f,g,i : constants in brackets, solve with top
    c = random.randint(-1,1)
    f = random.randint(-2,2)
    l = random.randint(-20,20)
    i = (top - j*l +a*c +d*f)/g
    question["answer_top"] = g*i + j*l - a*c - d*f
    
    global variables
    variables = [a,b,c,d,e,f,g,h,i,j,k,l]
    question["question"] = "%d(%dt + %d) + %d(%dt + %d)  = %d(%dt + %d) + %d(%dt + %d)" %(a,b,c,d,e,f,g,h,i,j,k,l)
    global correct_answer
    correct_answer = question["answer"]
    questions = []
    questions.append(question)
    return render(request, 'module1/module1_1d.html', {'questions':questions})

def answer1_1d(request): 
    question = "%d(%dt + %d) + %d(%dt + %d)  = %d(%dt + %d) + %d(%dt + %d)" %(variables[0],variables[1],variables[2],variables[3],variables[4],variables[5], \
        variables[6], variables[7],variables[8],variables[9],variables[10],variables[11])
    answerGiven = float(request.POST['answer'])
    answerOriginal = round(float(correct_answer),2)
    answerDiv = round(1/answerOriginal,2)
    if answerGiven == answerOriginal:
        text = "Jouw antwoord was goed!"
        hint = "Doe de vraag nog een keer, of ga naar de volgende vraag."
    elif answerGiven == - answerOriginal:
        text = "Jouw antwoord niet goed."
        hint = "Maar bijna goed, let op met plus- en mintekens wegstrepen."
    elif answerGiven == answerDiv:
        text = "Jouw antwoord was fout."
        hint = "Let op met delen."
    else:
       text = "Jouw antwoord was fout." 
       hint = "Werk eerst de haakjes weg."
    
    return render(request, 'accounts/answers/answer1_1d.html', {'answerGiven':answerGiven, 'answerOriginal':answerOriginal, \
        'text': text, 'hint': hint, 'question': question})

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

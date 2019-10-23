# accounts/views.py
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render
from django.http import HttpResponse
from .models import CustomUser, ModuleOverview, Module, SubModule, Exam
from .forms import AnswerForm, CustomUserCreationForm, CustomUserChangeForm
import random, sqlite3, getpass
from sqlite3 import Error
from django.shortcuts import redirect
#import numpy as np
database = r"db.sqlite3"

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
    if(user[1] == 1):    
        sql = """INSERT INTO accounts_module_user (user_id, currentModule, amountCorrect, amountWrong, amountHints, moduleScore, module_id, mistake1, mistake2, mistake3, mistake4, mistake5, currentQuestionHints, currentQuestionCorrect)
                                VALUES (?, 1, 0, 0, 0, 0, ?, 0, 0, 0, 0, 0, 0, 0) """
    else:
        sql = """INSERT INTO accounts_module_user (user_id, currentModule, amountCorrect, amountWrong, amountHints, moduleScore, module_id, mistake1, mistake2, mistake3, mistake4, mistake5, currentQuestionHints, currentQuestionCorrect)
                                VALUES (?, 0, 0, 0, 0, 0, ?, 0, 0, 0, 0, 0, 0, 0) """
    cur = conn.cursor()
    cur.execute(sql, user)
    return cur.lastrowid

def insertNewUser(user_id):
    #database = r"C:/MathApp/accounts/db.sqlite3"
    #database = r"C:/Users/s162449/Documents/Uni/year-4/quartile-1/0LAUK0-Robots-everywhere/accounts-Github/accounts/db.sqlite3"

    # create a database connection
    conn = create_connection(database)

    modules = Module.objects.all()
    for module in modules:
        with conn:
            # create a new project
            user_Module = (user_id, module.id)
            addModule = create_user(conn, user_Module)
 
def AnswerAnswered(user_id, module_id, correct, hintsUsed, mistakeNr):
    #database = r"C:/Users/s162449/Documents/Uni/year-4/quartile-1/0LAUK0-Robots-everywhere/accounts-Github/accounts/db.sqlite3"
    #database = r"C:/MathApp/accounts/db.sqlite3"
    # create a database connection
    conn = create_connection(database)

    with conn:
        # create a new project
        amountMistake = answerAnsweredDatabase(conn, user_id, module_id, correct, hintsUsed, mistakeNr)
    
    return amountMistake

def answerAnsweredDatabase(conn, user_id, module_id, correct, hintsUsed, mistakeNr):
    user_module = (user_id, module_id)
    if correct:
        sql_request_amount = 'SELECT amountCorrect, amountHints, currentQuestionHints, currentQuestionCorrect, mistake1 FROM accounts_module_user WHERE user_id = ? AND module_id = ?'
    else:
        if mistakeNr == 1:
            sql_request_amount = 'SELECT amountWrong, amountHints, currentQuestionHints, currentQuestionCorrect, mistake1 FROM accounts_module_user WHERE user_id = ? AND module_id = ?'
        elif mistakeNr == 2:
            sql_request_amount = 'SELECT amountWrong, amountHints, currentQuestionHints, currentQuestionCorrect, mistake2 FROM accounts_module_user WHERE user_id = ? AND module_id = ?'
        elif mistakeNr == 3:
            sql_request_amount = 'SELECT amountWrong, amountHints, currentQuestionHints, currentQuestionCorrect, mistake3 FROM accounts_module_user WHERE user_id = ? AND module_id = ?'
        elif mistakeNr == 4:
            sql_request_amount = 'SELECT amountWrong, amountHints, currentQuestionHints, currentQuestionCorrect, mistake4 FROM accounts_module_user WHERE user_id = ? AND module_id = ?'
        elif mistakeNr == 5:
            sql_request_amount = 'SELECT amountWrong, amountHints, currentQuestionHints, currentQuestionCorrect, mistake5 FROM accounts_module_user WHERE user_id = ? AND module_id = ?'
        elif mistakeNr == 6:
            sql_request_amount = 'SELECT amountWrong, amountHints, currentQuestionHints, currentQuestionCorrect, mistake1, mistake2 FROM accounts_module_user WHERE user_id = ? AND module_id = ?'
        else:
            sql_request_amount = 'SELECT amountWrong, amountHints, currentQuestionHints, currentQuestionCorrect, mistake1 FROM accounts_module_user WHERE user_id = ? AND module_id = ?'


    cur = conn.cursor()
    cur.execute(sql_request_amount, user_module)
    records = cur.fetchall()
    if(correct):
        newCurrentQuestionCorrect = records[0][3]+1
        newMistakeX = records[0][4]
    else:
        newCurrentQuestionCorrect = records[0][3]
        if mistakeNr == 0:
            newMistakeX = records[0][4]
        else:
            newMistakeX = records[0][4]+1
    newAmountHints = records[0][1]+hintsUsed
    newcurrentQuestionHints = records[0][2]+hintsUsed
    newAmountCorrect_Wrong = records[0][0]+1
    if correct:
        newcorrect = [newAmountCorrect_Wrong, newAmountHints, newcurrentQuestionHints, newCurrentQuestionCorrect, user_id, module_id]
        amountMaxMistake = 0
    elif mistakeNr == 6:
        newMistakeY = records[0][5]+1
        newcorrect = [newAmountCorrect_Wrong, newAmountHints, newcurrentQuestionHints, newCurrentQuestionCorrect, newMistakeX, newMistakeY, user_id, module_id]
        amountMaxMistake = max(newMistakeX, newMistakeY)
    else:
        newcorrect = [newAmountCorrect_Wrong, newAmountHints, newcurrentQuestionHints, newCurrentQuestionCorrect, newMistakeX, user_id, module_id]
        amountMaxMistake = newMistakeX

    

    if correct:
        sql = 'UPDATE accounts_module_user SET amountCorrect = ?, amountHints = ?, currentQuestionHints = ?, currentQuestionCorrect = ? WHERE user_id = ? AND module_id = ?'
    else:
        if mistakeNr == 1:
            sql = 'UPDATE accounts_module_user SET amountWrong = ?, amountHints = ?, currentQuestionHints = ?, currentQuestionCorrect = ?, mistake1 = ? WHERE user_id = ? AND module_id = ?'
        elif mistakeNr == 2:
            sql = 'UPDATE accounts_module_user SET amountWrong = ?, amountHints = ?, currentQuestionHints = ?, currentQuestionCorrect = ?, mistake2 = ? WHERE user_id = ? AND module_id = ?'
        elif mistakeNr == 3:
            sql = 'UPDATE accounts_module_user SET amountWrong = ?, amountHints = ?, currentQuestionHints = ?, currentQuestionCorrect = ?, mistake3 = ? WHERE user_id = ? AND module_id = ?'
        elif mistakeNr == 4:
            sql = 'UPDATE accounts_module_user SET amountWrong = ?, amountHints = ?, currentQuestionHints = ?, currentQuestionCorrect = ?, mistake4 = ? WHERE user_id = ? AND module_id = ?'
        elif mistakeNr == 5:
            sql = 'UPDATE accounts_module_user SET amountWrong = ?, amountHints = ?, currentQuestionHints = ?, currentQuestionCorrect = ?, mistake5 = ? WHERE user_id = ? AND module_id = ?'
        elif mistakeNr == 6:
            sql = 'UPDATE accounts_module_user SET amountWrong = ?, amountHints = ?, currentQuestionHints = ?, currentQuestionCorrect = ?, mistake1 = ?, mistake2 = ? WHERE user_id = ? AND module_id = ?'
        else:
            sql = 'UPDATE accounts_module_user SET amountWrong = ?, amountHints = ?, currentQuestionHints = ?, currentQuestionCorrect = ?, mistake1 = ? WHERE user_id = ? AND module_id = ?'

    cur = conn.cursor()
    cur.execute(sql,newcorrect)
    return amountMaxMistake

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

def moduleCurrent(request):
    database = r"C:/Users/s162449/Documents/Uni/year-4/quartile-1/0LAUK0-Robots-everywhere/accounts-Github/accounts/db.sqlite3"
    #database = r"C:/MathApp/accounts/db.sqlite3"
    # create a database connection
    conn = create_connection(database)

    with conn:
        # create a new project
            currentModule = moduleCurrentDatabase(conn, request.user.id)
    if(currentModule[0]==1): 
        if(currentModule[1]==1):
            return redirect('/accounts/module1_1a/')
        if(currentModule[1]==2):
            return redirect('/accounts/module1_1b/')
        if(currentModule[1]==3):
            return redirect('/accounts/module1_1c/')
        if(currentModule[1]==4):
            return redirect('/accounts/module1_1d/')
    else:
        return redirect('/accounts/home')
    
  

def moduleCurrentDatabase(conn, user_id):
    inputQuery = [user_id]
    sql = 'SELECT module_id, currentModule FROM accounts_module_user WHERE user_id = ? AND currentModule > 0'

    cur = conn.cursor()
    cur.execute(sql, inputQuery)
    records = cur.fetchall()
    return records[0]


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

def IsNextQuestionPossible(user_id, module_id):
    #database = r"C:/Users/s162449/Documents/Uni/year-4/quartile-1/0LAUK0-Robots-everywhere/accounts-Github/accounts/db.sqlite3"

    # create a database connection
    conn = create_connection(database)
    user_module = (user_id, module_id)
    sql_request_amount = 'SELECT currentQuestionCorrect FROM accounts_module_user WHERE user_id = ? AND module_id = ?'
    cur = conn.cursor()
    cur.execute(sql_request_amount, user_module)
    records = cur.fetchall()
    currentQuestionCorrect = records[0][0]
    #THIS VALUE IS ADJUSTABLE
    amountCorrectBeforeNewQuestion = 2
    #Need more than the above value correct to continue
    if currentQuestionCorrect > amountCorrectBeforeNewQuestion:
        return True
    else:
        return False

def ResetCurrentQuestionCorrect(user_id, module_id, nextModule):
    #database = r"C:/Users/s162449/Documents/Uni/year-4/quartile-1/0LAUK0-Robots-everywhere/accounts-Github/accounts/db.sqlite3"

    # create a database connection
    conn = create_connection(database)

    with conn:
        # create a new project
            ResetCurrentQuestionCorrectDatabase(conn, user_id, module_id, nextModule)

def ResetCurrentQuestionCorrectDatabase(conn, user_id, module_id, nextModule):
    next_user_module = (nextModule, user_id, module_id)
    sql = 'UPDATE accounts_module_user SET currentQuestionHints = 0, currentQuestionCorrect = 0, currentModule = ?, mistake1 = 0, mistake2 = 0, mistake3 = 0, mistake4 = 0, mistake5 = 0 WHERE user_id = ? AND module_id = ?'

    cur = conn.cursor()
    cur.execute(sql,next_user_module)
       

def answer1_1a(request):
    question = "%sx + %s + %sx + %s" %(variables[0],variables[1],variables[2],variables[3])
    answerGiven = request.POST['answer_1'], request.POST['answer_2']
    answerOriginal = correct_answer
    user = request.user
    if answerGiven[0] != answerOriginal[0] and answerGiven[1] != answerOriginal[1]:
        correct = 0
        hint = "De x-termen én constanten zijn niet goed bij elkaar opgeteld."
        maxMistake = AnswerAnswered(user.id, 1, False, 0, 6)
    elif  answerGiven[0] != answerOriginal[0]:
        correct = 0
        hint = "De x-termen zijn niet goed opgeteld."
        maxMistake = AnswerAnswered(user.id, 1, False, 0, 2)
    elif answerGiven[1] != answerOriginal[1]:
        correct = 0
        maxMistake = AnswerAnswered(user.id, 1, False, 0, 1)
        hint = "De constanten zijn niet goed opgeteld."   
    elif answerGiven == answerOriginal:
        correct = 1
        hint = "Doe de vraag nog een keer, of ga naar de volgende vraag."
        maxMistake = AnswerAnswered(user.id, 1, True, 0, 0)
    else:
        correct = 0
        hint = "Let goed op de plus- en mintekens."
        maxMistake = AnswerAnswered(user.id, 1, False, 0, 0)

    print(maxMistake)
    if maxMistake > 2:
        toManyMistakes = True
    else:
        toManyMistakes = False
    
    print(toManyMistakes)
    
    nextQuestionPossible = IsNextQuestionPossible(user.id, 1)
    return render(request, 'accounts/answers/answer1_1a.html', {'answerGiven_1':answerGiven[0],'answerGiven_2':answerGiven[1], \
        'answerOriginal_1':answerOriginal[0], 'answerOriginal_2':answerOriginal[1],'correct': correct, 'hint': hint,
         'question': question, 'nextQuestionPossible':nextQuestionPossible, 'toManyMistakes': toManyMistakes})

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

def module1_1b_from_module1_1a(request):
    nextModule = 2
    ResetCurrentQuestionCorrect(request.user.id, 1, nextModule)
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
    question = "%sx + %s = %sx + %s" %(variables[0],variables[1],variables[2],variables[3])
    answerGiven = request.POST['answer_1'], request.POST['answer_2']
    answerOriginal = correct_answer
    if answerGiven[0] != answerOriginal[0] and answerGiven[1] != answerOriginal[1]:
        correct = 0
        hint = "Tel de x-termen goed op aan de linkerzijde. Tel de constanten goed op aan de rechterzijde. Let goed op plus- en mintekens."
        maxMistake = AnswerAnswered(request.user.id, 1, False, 0, 6)
    elif answerGiven[0] != answerOriginal[0]:
        correct = 0
        hint = "De linkerzijde heeft niet (alleen) het goede aantal x-termen. Let goed op plus- en mintekens."
        maxMistake = AnswerAnswered(request.user.id, 1, False, 0, 2)
    elif answerGiven[1] != answerOriginal[1]:
        correct = 0
        hint =  "De rechterzijde heeft niet de goede waarde, de constanten zijn niet goed opgeteld. Let goed op plus- en mintekens."
        maxMistake = AnswerAnswered(request.user.id, 1, False, 0, 1)
    elif answerGiven == answerOriginal:
        correct = 1
        hint = ""
        maxMistake = AnswerAnswered(request.user.id, 1, True, 0, 0)
    else:
        correct = 0
        maxMistake = AnswerAnswered(request.user.id, 1, False, 0, 0)
        hint = "Doe de vraag nog een keer, of ga naar de volgende vraag."

    if maxMistake > 2:
        toManyMistakes = True
    else:
        toManyMistakes = False

    nextQuestionPossible = IsNextQuestionPossible(request.user.id, 1)
    return render(request, 'accounts/answers/answer1_1b.html', {'answerGiven_1':answerGiven[0],'answerGiven_2':answerGiven[1], \
        'answerOriginal_1':answerOriginal[0], 'answerOriginal_2':answerOriginal[1],'correct': correct, 'hint': hint, 'question': question,
         'nextQuestionPossible':nextQuestionPossible, 'toManyMistakes': toManyMistakes})

def module1_1c(request):
    question = {}
    question["answer"] = random.randint(-20,20)
    if  question["answer"]==0:
        question["answer"] = 1
    left = random.randint(-10,10)
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

def module1_1c_from_module1_1b(request):
    nextModule = 3
    ResetCurrentQuestionCorrect (request.user.id, 1, nextModule)
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
    global variables
    variables = [a,b,c,d]
    question["question"] = "%sy + %s = %sy + %s" %(a,b,c,d)  #vary which terms have 'x'? # vary name 'x', # +- = -
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
        correct = 1
        hint = "Doe de vraag nog een keer, of ga naar de volgende vraag."
        maxMistake = AnswerAnswered(request.user.id, 1, True, 0, 0)
    elif answerGiven == float(round(( variables[3] + variables[1] )/ (variables[0] + variables[2] ), 2)):
        correct = 0
        hint = "Let goed op plus- en mintekens bij het omzetten van beide termen."
        maxMistake = AnswerAnswered(request.user.id, 1, False, 0, 6)
    elif answerGiven == float(round((  variables[3] + variables[1] )/ (variables[0] - variables[2] ),2)):
        correct = 0
        hint = "Let goed op met het optellen of aftrekken van de constanten."
        maxMistake = AnswerAnswered(request.user.id, 1, False, 0, 1)
    elif answerGiven == float(round(( variables[3] - variables[1] )/ (variables[0] + variables[2] ), 2)):
        correct = 0
        hint = "Let goed op met het optellen of aftrekken van de x-termen."
        maxMistake = AnswerAnswered(request.user.id, 1, False, 0, 2)
    elif answerGiven == answerDiv:
        correct = 0
        hint = "Let op met delen."
        maxMistake = AnswerAnswered(request.user.id, 1, False, 0, 3)
    else:
       correct = 0 
       hint = "Let goed op de plus- en mintekens."
       maxMistake = AnswerAnswered(request.user.id, 1, False, 0, 0)

    if maxMistake > 2 & (answerGiven != answerOriginal):
        toManyMistakes = True
    else:
        toManyMistakes = False
    
    nextQuestionPossible = IsNextQuestionPossible(request.user.id, 1)
    return render(request, 'accounts/answers/answer1_1c.html', {'answerGiven':answerGiven, 'answerOriginal':answerOriginal, \
        'correct': correct, 'hint': hint, 'question': question, 'nextQuestionPossible':nextQuestionPossible, 'toManyMistakes': toManyMistakes})

def module1_1d(request): #nu nog een copy van c.
    question = {}
    question["answer"] = random.randint(-20,20)
    if  question["answer"]==0:
        question["answer"] = 1
    left = random.randint(-10,10)
    right = left*question["answer"]
    c = random.randint(-20,20)
    a = left + c
    b = random.randint(-20,20)
    d = right + b
    global variables
    variables = [a,b,c,d]
    question["question"] = "%sy + %s = %sy + %s" %(a,b,c,d)  #vary which terms have 'x'? # vary name 'x', # +- = -
    question["answer_1"] = a - c
    question["answer_2"] = d - b
    global correct_answer
    correct_answer = question["answer"]
    questions = []
    questions.append(question)

    return render(request, 'module1/module1_1d.html', {'questions':questions})

def module1_1d_from_module1_1c(request): #nu nog een copy van c.
    nextModule = 4
    ResetCurrentQuestionCorrect (request.user.id, 1, nextModule)
    question = {}
    question["answer"] = random.randint(-20,20)
    if  question["answer"]==0:
        question["answer"] = 1
    left = random.randint(-10,10)
    right = left*question["answer"]
    c = random.randint(-20,20)
    a = left + c
    b = random.randint(-20,20)
    d = right + b
    global variables
    variables = [a,b,c,d]
    question["question"] = "%sy + %s = %sy + %s" %(a,b,c,d)  #vary which terms have 'x'? # vary name 'x', # +- = -
    question["answer_1"] = a - c
    question["answer_2"] = d - b
    global correct_answer
    correct_answer = question["answer"]
    questions = []
    questions.append(question)

    return render(request, 'module1/module1_1d.html', {'questions':questions})

def answer1_1d(request): # nu nog een copy van c.
    question = "%sy + %s = %sy + %s" %(variables[0],variables[1],variables[2],variables[3])
    answerGiven = float(request.POST['answer'])
    answerOriginal = float(correct_answer)
    answerDiv = round(1/answerOriginal,2)
    if answerGiven == answerOriginal:
        correct = 1
        hint = "Doe de vraag nog een keer, of ga naar de volgende vraag."
        maxMistake = AnswerAnswered(request.user.id, 1, True, 0, 0)
    elif answerGiven == float(round(( variables[3] + variables[1] )/ (variables[0] + variables[2] ), 2)):
        correct = 0
        hint = "Let goed op plus- en mintekens bij het omzetten van beide termen."
        maxMistake =AnswerAnswered(request.user.id, 1, False, 0, 6)
    elif answerGiven == float(round((  variables[3] + variables[1] )/ (variables[0] - variables[2] ),2)):
        correct = 0
        hint = "Let goed op met het optellen of aftrekken van de constanten."
        maxMistake = AnswerAnswered(request.user.id, 1, False, 0, 1)
    elif answerGiven == float(round(( variables[3] - variables[1] )/ (variables[0] + variables[2] ), 2)):
        correct = 0
        hint = "Let goed op met het optellen of aftrekken van de x-termen."
        maxMistake = AnswerAnswered(request.user.id, 1, False, 0, 2)
    elif answerGiven == answerDiv:
        correct = 0
        hint = "Let op met delen."
        maxMistake = AnswerAnswered(request.user.id, 1, False, 0, 3)
    else:
       correct = 0 
       hint = "Let goed op de plus- en mintekens."
       maxMistake = AnswerAnswered(request.user.id, 1, False, 0, 0)

    if maxMistake > 2:
        toManyMistakes = True
    else:
        toManyMistakes = False

    nextQuestionPossible = IsNextQuestionPossible(request.user.id, 1)
    
    return render(request, 'accounts/answers/answer1_1d.html', {'answerGiven':answerGiven, 'answerOriginal':answerOriginal, \
        'correct': correct, 'hint': hint, 'question': question,  'nextQuestionPossible':nextQuestionPossible, 'toManyMistakes': toManyMistakes})

def module1_2(request):
    text = "Wat is het goede antwoord " # % number
    return render(request,'module1/module1_1.html', {'vraag': text} )

def module1_2_from_module1_1d(request):
    nexModule = 0
    ResetCurrentQuestionCorrect(request.user.id, 1, nextModule)
    text = "Wat is het goede antwoord " # % number
    return render(request, 'module1/module1_2.html', {'questions':questions})

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
        AnswerAnswered(request.user.id, module_id, True, 0)

    else:
        text = "your answer was wrong"
        AnswerAnswered(request.user.id, module_id, False, 0)

    return render(request, 'accounts/answer.html', {'answerGiven':answerGiven, 'answerOriginal':answerOriginal, 'text': text})

def teacherOverview(request):
    isTeacher = IsTeacher(request.user.id)
    if isTeacher:
        records = GetAllInfo()
        return render(request, 'teacher.html',{'records':records})
    else:
        return render(request, 'teacherconformation.html')
    
def GetAllInfo():
    database = r"C:/Users/s162449/Documents/Uni/year-4/quartile-1/0LAUK0-Robots-everywhere/accounts-Github/accounts/db.sqlite3"
    #database = r"C:/MathApp/accounts/db.sqlite3"
    # create a database connection
    conn = create_connection(database)

    with conn:
        # create a new project
            return GetAllInfoDatabase(conn)

def GetAllInfoDatabase(conn):
    #sql = 'SELECT username, generalIntelligence FROM accounts_customuser WHERE isTeacher = 0'
    sql = 'SELECT username, generalIntelligence, id FROM accounts_customuser WHERE isTeacher = 0'
    
    cur = conn.cursor()
    cur.execute(sql)
    records = cur.fetchall()
    recordsWithValue = []

    for record in records:
        inputQuery = [record[2]]
        sqlAmount = 'SELECT amountCorrect, amountWrong FROM accounts_module_user WHERE user_id = ?'
        cur = conn.cursor()
        cur.execute(sqlAmount,inputQuery)
        newRecords = cur.fetchall()
        totalCorrect = 0
        totalWrong = 0
        for newrecord in newRecords:
            totalCorrect = totalCorrect + newrecord[0]
            totalWrong = totalWrong + newrecord[1]
        recordsWithValue.append([record[0],record[1],totalCorrect,totalWrong])
    return recordsWithValue

def IsTeacher(user_id):
    database = r"C:/Users/s162449/Documents/Uni/year-4/quartile-1/0LAUK0-Robots-everywhere/accounts-Github/accounts/db.sqlite3"
    #database = r"C:/MathApp/accounts/db.sqlite3"
    # create a database connection
    conn = create_connection(database)

    with conn:
        # create a new project
             return IsTeacherDatabase(conn, user_id)

def IsTeacherDatabase(conn, user_id):
    inputQuery = [user_id]
    sql = 'SELECT isTeacher FROM accounts_customuser WHERE id = ?'

    cur = conn.cursor()
    cur.execute(sql, inputQuery)
    records = cur.fetchall()
    return records[0][0]

def confirmTeacher(request):
    passwordGiven= request.POST['password']
    password = "Lerarerzijnhetbeste!"
    user = request.user.id
    if passwordGiven == password:
        MakeTeacher(user)
        return render(request, 'teacher.html')
    else:
        alert("this password was incorrect")
    

def MakeTeacher(user_id):
    database = r"C:/Users/s162449/Documents/Uni/year-4/quartile-1/0LAUK0-Robots-everywhere/accounts-Github/accounts/db.sqlite3"
    #database = r"C:/MathApp/accounts/db.sqlite3"
    # create a database connection
    conn = create_connection(database)

    with conn:
        # create a new project
             return MakeTeacherDatabase(conn, user_id)

def MakeTeacherDatabase(conn, user_id):
    print(user_id)
    inputQuery = [user_id]
    sql = 'UPDATE accounts_customuser SET isTeacher = True WHERE id = ?'

    cur = conn.cursor()
    cur.execute(sql,inputQuery)

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

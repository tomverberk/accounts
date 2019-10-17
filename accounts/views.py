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
    sql = """INSERT INTO accounts_module_user (user_id, currentModule, amountCorrect, amountWrong, amountHints, moduleScore, module_id, mistake1, mistake2, mistake3, mistake4, mistake5, currentQuestionHints, currentQuestionCorrect)
                                VALUES (?, false, 0, 0, 0, 0, ?, 0, 0, 0, 0, 0, 0, 0) """
    cur = conn.cursor()
    cur.execute(sql, user)
    return cur.lastrowid

def insertNewUser(user_id):
    #database = r"C:/MathApp/accounts/db.sqlite3"
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
 
def AnswerAnswered(user_id, module_id, correct, hintsUsed, mistakeNr):
    #database = r"C:/Users/s162449/Documents/Uni/year-4/quartile-1/0LAUK0-Robots-everywhere/accounts-Github/accounts/db.sqlite3"
    #database = r"C:/MathApp/accounts/db.sqlite3"
    # create a database connection
    conn = create_connection(database)

    with conn:
        # create a new project
            answerAnsweredDatabase(conn, user_id, module_id, correct, hintsUsed, mistakeNr)

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
    elif mistakeNr == 6:
        newMistakeY = records[0][5]+1
        newcorrect = [newAmountCorrect_Wrong, newAmountHints, newcurrentQuestionHints, newCurrentQuestionCorrect, newMistakeX, newMistakeY, user_id, module_id]
    else:
        newcorrect = [newAmountCorrect_Wrong, newAmountHints, newcurrentQuestionHints, newCurrentQuestionCorrect, newMistakeX, user_id, module_id]

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
            print(mistakeNr)
            print(correct)
            sql = 'UPDATE accounts_module_user SET amountWrong = ?, amountHints = ?, currentQuestionHints = ?, currentQuestionCorrect = ?, mistake1 = ?, mistake2 = ? WHERE user_id = ? AND module_id = ?'
        else:
            sql = 'UPDATE accounts_module_user SET amountWrong = ?, amountHints = ?, currentQuestionHints = ?, currentQuestionCorrect = ?, mistake1 = ? WHERE user_id = ? AND module_id = ?'

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

def ResetCurrentQuestionCorrect(user_id, module_id):
    #database = r"C:/Users/s162449/Documents/Uni/year-4/quartile-1/0LAUK0-Robots-everywhere/accounts-Github/accounts/db.sqlite3"

    # create a database connection
    conn = create_connection(database)

    with conn:
        # create a new project
            ResetCurrentQuestionCorrectDatabase(conn, user_id, module_id)

def ResetCurrentQuestionCorrectDatabase(conn, user_id, module_id):
    user_module = (user_id, module_id)
    sql = 'UPDATE accounts_module_user SET currentQuestionHints = 0, currentQuestionCorrect = 0 WHERE user_id = ? AND module_id = ?'

    cur = conn.cursor()
    cur.execute(sql,user_module)
       

def answer1_1a(request):
    question = "%sx + %s + %sx + %s" %(variables[0],variables[1],variables[2],variables[3])
    answerGiven = request.POST['answer_1'], request.POST['answer_2']
    answerOriginal = correct_answer
    user = request.user
    if answerGiven[0] != answerOriginal[0] and answerGiven[1] != answerOriginal[1]:
        text = "Jouw antwoord was fout."
        hint = "De x-termen én constanten zijn niet goed bij elkaar opgeteld."
        AnswerAnswered(user.id, 1, False, 0, 6)
    elif  answerGiven[0] != answerOriginal[0]:
        text = "Jouw antwoord was fout."
        hint = "De x-termen zijn niet goed opgeteld."
        AnswerAnswered(user.id, 1, False, 0, 2)
    elif answerGiven[1] != answerOriginal[1]:
        text = "Jouw antwoord was fout."
        hint = "De constanten zijn niet goed opgeteld."
        AnswerAnswered(user.id, 1, False, 0, 1)
    elif answerGiven == answerOriginal:
        text = "Jouw antwoord was goed!"
        hint = "Doe de vraag nog een keer, of ga naar de volgende vraag."
        AnswerAnswered(user.id, 1, True, 0, 0)
    else:
        text = "Jouw antwoord was fout."
        hint = "Let goed op de plus- en mintekens."
        AnswerAnswered(user.id, 1, False, 0, 0)
    
    nextQuestionPossible = IsNextQuestionPossible(user.id, 1)
    return render(request, 'accounts/answers/answer1_1a.html', {'answerGiven_1':answerGiven[0],'answerGiven_2':answerGiven[1], \
        'answerOriginal_1':answerOriginal[0], 'answerOriginal_2':answerOriginal[1],'text': text, 'hint': hint, 'question': question, 'nextQuestionPossible':nextQuestionPossible})

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
    ResetCurrentQuestionCorrect(request.user.id, 1)
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
        text = "Jouw antwoord was fout."
        hint = "Tel de x-termen goed op aan de linkerzijde. Tel de constanten goed op aan de rechterzijde. Let goed op plus- en mintekens."
        AnswerAnswered(request.user.id, 1, False, 0, 6)
    elif answerGiven[0] != answerOriginal[0]:
        text = "Jouw antwoord was fout."
        hint = "De linkerzijde heeft niet (alleen) het goede aantal x-termen. Let goed op plus- en mintekens."
        AnswerAnswered(request.user.id, 1, False, 0, 2)
    elif answerGiven[1] != answerOriginal[1]:
        text = "Jouw antwoord was fout."
        hint =  "De rechterzijde heeft niet de goede waarde, de constanten zijn niet goed opgeteld. Let goed op plus- en mintekens."
        AnswerAnswered(request.user.id, 1, False, 0, 1)
    elif answerGiven == answerOriginal:
        text = "Jouw antwoord was goed!"
        AnswerAnswered(request.user.id, 1, True, 0, 0)
    else:
        text = "Jouw antwoord was fout."
        AnswerAnswered(request.user.id, 1, False, 0, 0)
        hint = "Doe de vraag nog een keer, of ga naar de volgende vraag."


    nextQuestionPossible = IsNextQuestionPossible(request.user.id, 1)
    return render(request, 'accounts/answers/answer1_1b.html', {'answerGiven_1':answerGiven[0],'answerGiven_2':answerGiven[1], \
        'answerOriginal_1':answerOriginal[0], 'answerOriginal_2':answerOriginal[1],'text': text, 'hint': hint, 'question': question, 'nextQuestionPossible':nextQuestionPossible})

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
    ResetCurrentQuestionCorrect (request.user.id, 1)
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
    question = "%sy + %s = %sy + %s" %(variables[0],variables[1],variables[2],variables[3])
    answerGiven = float(request.POST['answer'])
    answerOriginal = float(correct_answer)
    answerDiv = round(1/answerOriginal,2)
    if answerGiven == answerOriginal:
        text = "Jouw antwoord was goed!"
        hint = "Doe de vraag nog een keer, of ga naar de volgende vraag."
        AnswerAnswered(request.user.id, 1, True, 0, 0)
    elif answerGiven == float(round(( variables[3] + variables[1] )/ (variables[0] + variables[2] ), 2)):
        text = "Jouw antwoord was fout."
        hint = "Let goed op plus- en mintekens bij het omzetten van beide termen."
        AnswerAnswered(request.user.id, 1, False, 0, 6)
    elif answerGiven == float(round((  variables[3] + variables[1] )/ (variables[0] - variables[2] ),2)):
        text = "Jouw antwoord was fout."
        hint = "Let goed op met het optellen of aftrekken van de constanten."
        AnswerAnswered(request.user.id, 1, False, 0, 1)
    elif answerGiven == float(round(( variables[3] - variables[1] )/ (variables[0] + variables[2] ), 2)):
        text = "Jouw antwoord was fout."
        hint = "Let goed op met het optellen of aftrekken van de x-termen."
        AnswerAnswered(request.user.id, 1, False, 0, 2)
    elif answerGiven == answerDiv:
        text = "Jouw antwoord was fout."
        hint = "Let op met delen."
        AnswerAnswered(request.user.id, 1, False, 0, 3)
    else:
       text = "Jouw antwoord was fout." 
       hint = "Let goed op de plus- en mintekens."
       AnswerAnswered(request.user.id, 1, False, 0, 0)
    
    nextQuestionPossible = IsNextQuestionPossible(request.user.id, 1)
    return render(request, 'accounts/answers/answer1_1c.html', {'answerGiven':answerGiven, 'answerOriginal':answerOriginal, \
        'text': text, 'hint': hint, 'question': question, 'nextQuestionPossible':nextQuestionPossible})

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

def answer1_1d(request): # nu nog een copy van c.
    question = "%sy + %s = %sy + %s" %(variables[0],variables[1],variables[2],variables[3])
    answerGiven = float(request.POST['answer'])
    answerOriginal = float(correct_answer)
    answerDiv = round(1/answerOriginal,2)
    if answerGiven == answerOriginal:
        text = "Jouw antwoord was goed!"
        hint = "Doe de vraag nog een keer, of ga naar de volgende vraag."
        AnswerAnswered(request.user.id, 1, True, 0, 0)
    elif answerGiven == float(round(( variables[3] + variables[1] )/ (variables[0] + variables[2] ), 2)):
        text = "Jouw antwoord was fout."
        hint = "Let goed op plus- en mintekens bij het omzetten van beide termen."
        AnswerAnswered(request.user.id, 1, False, 0, 6)
    elif answerGiven == float(round((  variables[3] + variables[1] )/ (variables[0] - variables[2] ),2)):
        text = "Jouw antwoord was fout."
        hint = "Let goed op met het optellen of aftrekken van de constanten."
        AnswerAnswered(request.user.id, 1, False, 0, 1)
    elif answerGiven == float(round(( variables[3] - variables[1] )/ (variables[0] + variables[2] ), 2)):
        text = "Jouw antwoord was fout."
        hint = "Let goed op met het optellen of aftrekken van de x-termen."
        AnswerAnswered(request.user.id, 1, False, 0, 2)
    elif answerGiven == answerDiv:
        text = "Jouw antwoord was fout."
        hint = "Let op met delen."
        AnswerAnswered(request.user.id, 1, False, 0, 3)
    else:
       text = "Jouw antwoord was fout." 
       hint = "Let goed op de plus- en mintekens."
       AnswerAnswered(request.user.id, 1, False, 0, 0)
    
    return render(request, 'accounts/answers/answer1_1d.html', {'answerGiven':answerGiven, 'answerOriginal':answerOriginal, \
        'text': text, 'hint': hint, 'question': question})

def module1_2(request):
    text = "Wat is het goede antwoord " # % number
    return render(request,'module1/module1_1.html', {'vraag': text} )

def module1_2_from_module1_1c(request):
    ResetCurrentQuestionCorrect(request.user.id, 1)
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
        AnswerAnswered(request.user.id, module_id, True, 0)

    else:
        text = "your answer was wrong"
        AnswerAnswered(request.user.id, module_id, False, 0)

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

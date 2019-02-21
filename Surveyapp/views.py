from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LoginForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Employee, SurveyQuestion, Survey, SurveyEmployee, Question,SurveyResponse
from django.core.mail import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from . errors import PasswordError

def index(request):
    return render(request, 'Surveyapp/home.html')


def question_list(request, survey_id):
    m = request.session['username']
    #emp = Employee.objects.get(emp_username=m)
    print(survey_id)

    emp_record = Question.objects.filter(surveyquestion__survey_id=survey_id)
    #question_all = Question.objects.all()
    #print("all ques",len(question_all))
    page = request.GET.get('page')
    paginator = Paginator(emp_record, 5)

    try:
        emp_record = paginator.page(page)
    except PageNotAnInteger:
        emp_record = paginator.page(1)
    except EmptyPage:
        emp_record = paginator.page(paginator.num_pages)

    context = {'session': m, 'survey_id': survey_id, 'question_list': emp_record}

    return render(request, 'Surveyapp/question_list.html', context)


def employee(request):
    m = request.session['username']
    emp = Employee.objects.get(emp_username=m)

    # survey_id = Category.objects.all()
    print(emp.id)
    emp_record = SurveyEmployee.objects.filter(employee=emp.id)
    #print(emp_record.survey_id)

    Completed_survey = list()
    incomplete_survey = list()
    assign_survey =list()
    total_survey =list()


    for survey in emp_record:
        print("surveyppppp",survey)
        survey_count = SurveyResponse.objects.filter(employee_id=emp.id, survey_id=survey.survey_id).count()
        print("survey_count*****", survey_count);

        if survey_count:
            if SurveyResponse.objects.filter(survey_id=survey.survey_id, employee_id=emp.id, SaveStatus=True):
                Completed_survey.append(survey)
            else:
                incomplete_survey.append(survey)
        else:
            #my_list = survey.extend(incomplete_survey)
            assign_survey.append(survey)

    incomplete_surveylen = len(incomplete_survey)
    Completed_surveylen = len(Completed_survey)
    assign_surveycount= len(assign_survey)
    assign_surveycount1 =assign_surveycount +1
    StatusCheck =SurveyResponse.objects.filter(survey_id=survey.survey_id, employee_id=emp.id)


    #print(StatusCheck)

    context = {'session': m, 'total_survey': total_survey,'StatusCheck': StatusCheck,'survey_list': emp_record,'completed_survey':Completed_survey,'incomplete_survey': incomplete_survey, 'assign_survey':assign_surveycount1,'complete_count': Completed_surveylen,'incomplete_count': incomplete_surveylen}
    print(emp_record)
    for i in emp_record:

        print("id :", i.survey_id)

    send_email(request)
    return render(request, "Surveyapp/survey.html", context)


def login(request):
    print("calling post method")
    form = LoginForm()
    context = {'form': form}
    #Flag = True
    if request.method == "POST":
        print("Entering into post method")

        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            if Employee.objects.get(emp_username=username, emp_password=password):
                m = request.session['username'] = username
                # m1 = {'session': m}

                print("Session Name = "+m)
                return redirect('employee')
        except PasswordError:
            raise PasswordError(msg="wrong password")
            return render(request, "Surveyapp/login.html", context)

    return render(request, "Surveyapp/login.html", context)


def save(request, survey_id):
    m = request.session['username']
    emp = Employee.objects.get(emp_username=m)
    print("hiii", emp, survey_id)

    #print("savebtn",int(request.POST.get('saveform')))
    if request.POST['submitform'] == "Save":
        print('user clicked save')
    else:
        print("fdsg")

    for name in request.POST:
        print("question id: ", name)
        if name != "csrfmiddlewaretoken" and name != "submitform":
            isRecord = SurveyResponse.objects.filter(survey=Survey.objects.get(id=survey_id),
                                                     employee=Employee.objects.get(id=emp.id),
                                                     question=Question.objects.get(id=name))
            #print("submit", request.POST.get('submitform'))

            if not isRecord:
                if request.POST[name]:
                    surveyResponseObj = SurveyResponse()
                    surveyResponseObj.survey = Survey.objects.get(id=survey_id)
                    print(surveyResponseObj.survey)
                    surveyResponseObj.employee = Employee.objects.get(id=emp.id)
                    print(surveyResponseObj.employee)
                    surveyResponseObj.question = Question.objects.get(id=name)
                    print(surveyResponseObj.question)
                    surveyResponseObj.response = request.POST[name]
                    if request.POST['submitform'] == "Save":
                        surveyResponseObj.SaveStatus = False
                    else:
                        surveyResponseObj.SaveStatus = True
                    surveyResponseObj.save()

    return redirect("employee")

def send_email(request):
    try:
        name = request.session['username']
        print("Email has been send to :  ", name)
        email = EmailMessage('Survey Link', 'http://127.0.0.1:8000/Surveyapp/login/', to=['shitalraut708@gmail.com'])
        print("hiiii",email)
        email.send()

        print("Email has been send to :  ", name)
        print("---------------mail sent---------------")

    except Exception as e:
        print(e)

    return redirect('employee')

def logout(request):
    try:
        del request.session['username']
    except KeyError:
        pass
    return redirect('login')
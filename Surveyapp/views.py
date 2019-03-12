from django.shortcuts import render, redirect
# from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import EmailMessage
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.base import MIMEBase
# from email import encoders
from .forms import LoginForm
from . errors import PasswordError
from .models import (Employee, SurveyQuestion, Survey, SurveyEmployee, Question, SurveyResponse)


def index(request):
    return render(request, 'Surveyapp/home.html')


def question_list(request, survey_id):
    m = request.session['username']
    emp = Employee.objects.get(emp_username=m)
    emp_record = Question.objects.filter(surveyquestion__survey_id=survey_id)
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
    emp_record = SurveyEmployee.objects.filter(employee=emp.id)
    Completed_survey = list()
    incomplete_survey = list()
    assign_survey = list()
    total_survey = list()

    for survey in emp_record:
        survey_count = SurveyResponse.objects.filter(employee_id=emp.id, survey_id=survey.survey_id).count()

        if survey_count:
            if SurveyResponse.objects.filter(survey_id=survey.survey_id, employee_id=emp.id, SaveStatus=True):
                Completed_survey.append(survey)
            else:
                incomplete_survey.append(survey)
        else:
            assign_survey.append(survey)

    incomplete_surveylen = len(incomplete_survey)
    completed_surveylen = len(Completed_survey)
    assign_surveycount= len(assign_survey)
    assign_surveycount1 = assign_surveycount + 1
    status_check = SurveyResponse.objects.filter(survey_id=survey.survey_id, employee_id=emp.id)

    context = {
        'session': m,
        'total_survey': total_survey,
        'StatusCheck': status_check,
        'survey_list': emp_record,
        'completed_survey': Completed_survey,
        'incomplete_survey': incomplete_survey,
        'assign_survey': assign_surveycount1,
        'complete_count': completed_surveylen,
        'incomplete_count': incomplete_surveylen}

    send_email(request)
    return render(request, "Surveyapp/survey.html", context)


def login(request):
    form = LoginForm()
    context = {'form': form}

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            if Employee.objects.get(emp_username=username, emp_password=password):
                request.session['username'] = username
                return redirect('employee')
        except PasswordError:
            raise PasswordError(msg="wrong password")

    return render(request, "Surveyapp/login.html", context)


def save(request, survey_id):
    m = request.session['username']
    emp = Employee.objects.get(emp_username=m)

    for name in request.POST:
        if name != "csrfmiddlewaretoken" and name != "submitform":
            isRecord = SurveyResponse.objects.filter(survey=Survey.objects.get(id=survey_id),
                                                     employee=Employee.objects.get(id=emp.id),
                                                     question=Question.objects.get(id=name))

            if not isRecord:
                if request.POST[name]:
                    survey_response_obj = SurveyResponse()
                    survey_response_obj.survey = Survey.objects.get(id=survey_id)
                    survey_response_obj.employee = Employee.objects.get(id=emp.id)
                    survey_response_obj.question = Question.objects.get(id=name)
                    survey_response_obj.response = request.POST[name]
                    if request.POST['submitform'] == "Save":
                        survey_response_obj.SaveStatus = False
                    else:
                        survey_response_obj.SaveStatus = True
                    survey_response_obj.save()

    return redirect("employee")


def send_email(request):
    try:
        name = request.session['username']
        print("Email has been send to :  ", name)
        email = EmailMessage('Survey Link', 'http://127.0.0.1:8000/Surveyapp/login/', to=['shitalraut708@gmail.com'])
        email.send()

        print("Email has been send to :  ", name)
        print("---------------mail sent---------------")

    except Exception as e:
        print("Error:", str(e))

    return redirect('employee')


def logout(request):
    try:
        del request.session['username']
    except KeyError:
        pass
    return redirect('login')


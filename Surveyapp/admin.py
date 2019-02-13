from django.contrib import admin
from .models import Employee, Organization,Survey,Question,SurveyEmployee, SurveyQuestion,SurveyResponse

admin.site.register(Employee)
admin.site.register(Organization)
admin.site.register(SurveyQuestion)
admin.site.register(Question)
admin.site.register(Survey)
admin.site.register(SurveyEmployee)
admin.site.register(SurveyResponse)

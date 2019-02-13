from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('employee/', views.employee, name='employee'),
    path('login/', views.login, name='login'),
    path('que_list/<int:survey_id>', views.question_list, name='que_list'),
    path('save/<int:survey_id>', views.save, name='save'),
    path('logout/', views.logout, name='logout'),
    path('sendmail/', views.send_email, name='sendmail'),
]
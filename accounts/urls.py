# accounts/urls.py
from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.signUp, name='signup'),
    path('showInfo/', views.showInfo, name='showInfo'),
    path('exampleQuestion', views.exampleQuestion, name='exampleQuestion'),
    path('answer/', views.answer, name='answer'),
]
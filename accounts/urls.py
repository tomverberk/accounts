# accounts/urls.py

from django.urls import path
from django.views.generic import TemplateView
from django.conf.urls import include, url
from django.contrib import admin
admin.autodiscover()

from . import views


urlpatterns = [
    path('signup/', views.signUp, name='signup'),
    path('showInfo/', views.showInfo, name='showInfo'),
    path('teacherOverview', views.teacherOverview, name='teacherOverview'),
    path('confirmTeacher', views.confirmTeacher, name='confirmTeacher'),
    path('exampleQuestion', views.exampleQuestion, name='exampleQuestion'),
    #path('answer/', views.answer, name='answer'),
    path('moduleOverview/', views.moduleOverview, name='moduleOverview'),
    path('moduleCurrent/', views.moduleCurrent, name='moduleCurrent'),
    path('module1', views.module1, name='module1'),
    path('module1_1/', views.module1_1, name='module1_1'),
    path('module1_1a/', views.module1_1a, name='module1_1a'),
    path('module1_1a/answer/', views.answer1_1a, name='answer1_1a'),
    path('module1_1b/', views.module1_1b, name='module1_1b'),
    path('module1_1b/answer/', views.answer1_1b, name='answer1_1b'),
    path('module1_1b_from_module1_1a', views.module1_1b_from_module1_1a, name='module1_1b_from_module1_1a'),
    path('module1_1b_from_module1_1a/answer/', views.answer1_1b, name='answer1_1b'),
    path('module1_1c/', views.module1_1c, name='module1_1c'),
    path('module1_1c/answer/', views.answer1_1c, name='answer1_1c'),
    path('module1_1c_from_module1_1b', views.module1_1c_from_module1_1b, name='module1_1c_from_module1_1b'),
    path('module1_1c_from_module1_1b/answer/', views.answer1_1c, name='answer1_1c'),
    path('module1_1d/', views.module1_1d, name='module1_1d'),
    path('module1_1d/answer/', views.answer1_1d, name='answer1_1d'),
    path('module1_1d_from_module1_1c', views.module1_1d_from_module1_1c, name='module1_1d_from_module1_1c'),
    path('module1_1d_from_module1_1c/answer/', views.answer1_1d, name='module1_1d_from_module1_1c'),
    
    path('module1_2/', views.module1_2, name='module1_2'),
    path('module1_2_from_module1_1d', views.module1_2_from_module1_1d, name='module1_2_from_module_1_1d'),

    path('module1_3/', views.module1_3, name='module1_3'),
    path('module1_4/', views.module1_4, name='module1_4'),
    path('module1_5/', views.module1_5, name='module1_5'),
    path('module1_exam/', views.module1_exam, name='module1_exam'),

]
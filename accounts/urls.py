# accounts/urls.py

from django.urls import path
from django.views.generic import TemplateView
from django.conf.urls import include, url
from django.contrib import admin
admin.autodiscover()

from . import views


urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('showInfo/', views.showInfo, name='showInfo'),
    
    path('moduleOverview/', views.moduleOverview, name='moduleOverview'),
    path('module1/', views.module1, name='module1'),
    path('module1_1/', views.module1_1, name='module1_1'),
    path('module1_2/', views.module1_2, name='module1_2'),
    path('module1_3/', views.module1_3, name='module1_3'),
    path('module1_4/', views.module1_4, name='module1_4'),
    path('module1_5/', views.module1_5, name='module1_5'),
    path('module1_exam/', views.module1_exam, name='module1_exam'),
]
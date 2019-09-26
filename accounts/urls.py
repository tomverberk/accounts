# accounts/urls.py
from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('showInfo/', views.showInfo, name='showInfo'),
    
    path('moduleOverview/', views.ModuleOverview, name='moduleOverview'),
    path('module1/', views.Module1, name='module1'),
    path('module1_1/', views.Module1_1, name='module1_1'),
    path('module1_2/', views.Module1_2, name='module1_2'),
    path('module1_3/', views.Module1_3, name='module1_3'),
    path('module1_4/', views.Module1_4, name='module1_4'),
    path('module1_5/', views.Module1_5, name='module1_5'),
    path('module1_6/', views.Module1_6, name='module1_6'),
    path('module1_exam/', views.Module1_exam, name='module1_exam')
        
]
# accounts/urls.py

from django.urls import path
from django.views.generic import TemplateView

from . import views


urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('showInfo/', views.showInfo, name='showInfo'),
    
    path('moduleOverview/', views.moduleOverview, name='moduleOverview'),
    path('module1/', TemplateView.as_view(template_name="module1.html")),
    path('module1_1/', TemplateView.as_view(template_name="module1_1.html")),
    path('module1_2/', TemplateView.as_view(template_name="module1_2.html")),
    path('module1_3/', TemplateView.as_view(template_name="module1_3.html")),
    path('module1_4/', TemplateView.as_view(template_name="module1_4.html")),
    path('module1_5/', TemplateView.as_view(template_name="module1_5.html")),
    path('module1_exam/', TemplateView.as_view(template_name="module1_exam.html"))
        
]
"""
URL configuration for FinPal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path
from . import views  

urlpatterns = [
    path('', views.home_view, name='home'),
    path('chat', views.chat, name='chat'),
    path('login', views.login_view, name='login'),
    path('loginCheck', views.loginCheck, name="loginCheck"),
    path('dashboard', views.dashboardView, name="dashboard"),
    path('api/message/', views.chat_with_bot, name='chat_with_bot'),    
]

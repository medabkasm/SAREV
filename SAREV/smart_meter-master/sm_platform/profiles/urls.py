from django.contrib import admin
from django.urls import path , include , reverse_lazy , re_path
from .views import *
from django.contrib.auth import views as auth_views


app_name = 'profiles'

urlpatterns = [
    path('redirect/',redirect_profile,name = 'redirect_profile'),
    path('<str:username>/',profile_view,name = 'profile'),
    path('<str:username>/complete/',profile_complete,name = 'profile_complete'),
    ]

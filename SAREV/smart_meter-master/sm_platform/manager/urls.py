from django.contrib import admin
from django.urls import path , include , reverse_lazy , re_path
from .views import *
from django.contrib.auth import views as auth_views


app_name = 'manager'

urlpatterns = [
    path('add_data/<distributerName>/<distributerPass>/<meterNumber>/<voltage>/<current>/',add_data,name ='add_data'),
    path('get_bill/<str:username>/<id>/',get_bill,name='get_bill'),
    path('check_user/<str:username>/',check_user,name = 'check_user'),
    path('check_bill/<int:id>/',check_bill,name = 'check_bill'),
    path('user_profile/<str:username>/',user_profile,name = 'user_profile'),
    path('user_bill/<int:id>/',user_bill,name = 'user_bill'),
    path('ajax/bills/',ajax_bills_emp,name  = 'ajax_bills_emp'),
    path('ajax/users/',ajax_users,name = 'ajax_users'),
    path('ajax/user/',ajax_user,name = 'ajax_user'),
    path('dash_board/<str:username>/',dash_board,name='dash_board'),
    path('ajax/normal_user/chart/',ajax_chart,name='ajax_chart'),

    ]

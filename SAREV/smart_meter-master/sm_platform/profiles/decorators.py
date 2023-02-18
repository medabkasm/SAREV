from functools import wraps
from accounts.models import User
from django.shortcuts import  redirect


def profile_complete(function):
    def wrap(request, *args, **kwargs):
        user = User.objects.get(username = request.user.username)
        if request.user.is_authenticated:
            if user.profile.profileComplete:
                return function(request, *args, **kwargs)
            else:
                return redirect("profiles:profile_complete",request.user.username)
        else:
            return function(request, *args, **kwargs)

    return wrap


def profile_complete_reverse(function):
    def wrap(request, *args, **kwargs):
        user = User.objects.get(username = request.user.username)
        if request.user.is_authenticated:
            if user.profile.profileComplete:
                return redirect("profiles:profile",request.user.username)
            else:
                return function(request, *args, **kwargs)
        else:
            return function(request, *args, **kwargs)

    return wrap


def distributer(function):
    def wrap(request, *args, **kwargs):
        return function(request, *args, **kwargs)
    return wrap

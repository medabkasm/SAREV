from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .decorators import *
from accounts.models import *
from .forms import *
from	django.utils.translation	import	gettext_lazy	as	_
from django.contrib import messages
from django.contrib.auth import authenticate


@login_required
@profile_complete
def profile_view(request,username):
    if request.user.username == username:
        user = User.objects.get(username = username)
        return render(request,'profiles/profile.html')
    else:
       return redirect("profiles:profile_complete",request.user.username)

@login_required
@profile_complete_reverse
def profile_complete(request,username):
    if request.method == "POST" and request.user.username == username :
        user = request.user
        profile = Profile.objects.get(user = user)

        profileForm = profileEditForm(request.POST,request.FILES ,instance = profile )
        print(profileForm)
        profileForm.meterNumber = user.phone
        print(profileForm)
        if profileForm.is_valid():
            profileForm.save()
            message = _("Your profile info was setted successfully.")
            messages.success(request,message)
            return redirect("profiles:profile",user)
        else:
            return render(request,"profiles/profile_complete.html",{"profileEditForm" : profileForm ,})
    else:
        profileForm = profileEditForm()
        return render(request,"profiles/profile_complete.html",{"profileEditForm" : profileForm ,})


@login_required
def redirect_profile(request):
    return redirect('profiles:profile',request.user.username)

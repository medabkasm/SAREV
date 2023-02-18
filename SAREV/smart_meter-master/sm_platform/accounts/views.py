from django.shortcuts import render , redirect
from django.template.loader import render_to_string
from django.views.generic import View
from .models import User,Profile
from .forms import *  # RegisterForm
from django.utils.encoding import force_bytes, force_text
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .token_generator import account_activation_token
from django.core.mail import EmailMessage
from	django.utils.translation	import	gettext_lazy	as	_
import requests
from django.conf import settings
from .decorators import check_recaptcha
from django.contrib import messages
from django.http import JsonResponse

# Create your views here.

class	RegisterView(View):
    def post(self,request):
        form = RegisterForm(request.POST)
        agree = request.POST.get('agree-term')

        if	form.is_valid()  and agree:
            # rechaptcha validation
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            # End reCAPTCHA validation

            if result['success']:
                #	Create	a	new	user	object	but	avoid	saving	it	yet
                new_user = form.save(commit=False)
                #	Set	the	chosen	password
                new_user.set_password(form.cleaned_data['password1'])
                #new_profile = profileForm.save()
                #new_user.profile = new_profile
                #	Save	the	User	object
                new_user.is_active = True
                new_user.save()
                message = _("Your account was created successfully , you can login now.")
                messages.success(request,message)
                return redirect("accounts:login")
            else:
                agreeErrorText = _("you must agree to all statements in Terms of service")
                recaptchaErrorText = _("Invalid reCAPTCHA. Please try again.")
                return render(request,'accounts/register.html',{'form':form,'recaptcha':recaptchaErrorText})

        else:
            agreeErrorText = _("you must agree to all statements in Terms of service")
            recaptchaErrorText = _("Invalid reCAPTCHA. Please try again.")
            return render(request,'accounts/register.html',{'form':form,'agreeError':agreeErrorText,'recaptcha':recaptchaErrorText})

    def get(self,request):
        if request.user.is_authenticated:
            return	redirect('profiles:profile',request.user.username)

        form = RegisterForm()
        return render(request,'accounts/register.html',{'form':form})


@login_required
def delete_account(request,username):
    if request.user.username == username:
        return render(request,'accounts/delete_account.html')


@login_required
def delete_account_confirm(request,username):
    if request.user.username == username:
        try:
            User.objects.get(username = username).delete()
            message = _("the Account was deleted successfully.")
            messages.success(request,message)
        except:
            message = _("Unable to delete your Account.")
            messages.warning(request,message)

        return redirect('accounts:login')

    return redirect('profiles:profile',request.user.username)

from .models import	User
from django.contrib.auth.backends import BaseBackend

class	EmailAuthBackend(BaseBackend):
    """
    Authenticate using ane-mail address.
    """
    def	authenticate(self,request,username=None,password=None):
        try:
            user = User.objects.get(email = username.lower() )
            if	user.check_password(password):
                return	user
            return	None
        except	User.DoesNotExist:
            return	None

    def	get_user(self,user_id):
        try:
            return	User.objects.get(pk=user_id)
        except	User.DoesNotExist:
            return	None

class	UserNameAuthBackend(BaseBackend):
    """
    Authenticate using username.
    """
    def	authenticate(self,request,username=None,password=None):
        try:
            user = User.objects.get(username = username )
            if	user.check_password(password):
                return	user
            return	None
        except	User.DoesNotExist:
            return	None

    def	get_user(self,user_id):
        try:
            return	User.objects.get(pk=user_id)
        except	User.DoesNotExist:
            return	None


class PhoneAuthBackend(BaseBackend):
    """
    Authenticate using a phone number.
    """
    def	authenticate(self,request,username=None,password=None):
        try:
            if username[0] == '0':
                username = username[1:]
            user = User.objects.get(phone = username)
            if	user.check_password(password):
                return	user
            return	None
        except	User.DoesNotExist:
            return	None

    def	get_user(self,user_id):
        try:
            return	User.objects.get(pk=user_id)
        except	User.DoesNotExist:
            return	None

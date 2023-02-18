
from django import forms
from accounts.models import *
from	django.utils.translation	import	gettext_lazy	as	_
from django import forms
from accounts.validators import *

class profileEditForm(forms.ModelForm):     # form for creating / editing  a profile
    class Meta:
        model = Profile
        fields = ('firstName','lastName','gender','birthday','address','profileImage')


class userEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','phone','email')


class addDataForm(forms.Form):
    meterNumber = models.CharField(max_length = 10 ,validators = [phone_number_validation,])
    voltage = models.FloatField()
    current = models.FloatField()

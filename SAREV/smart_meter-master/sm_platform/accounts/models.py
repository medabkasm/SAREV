from django.db import models
from django.contrib.auth.models import AbstractUser
from	django.utils.translation	import	gettext_lazy	as	_
from .validators import fake_email_validation , phone_number_validation
from django.template.defaultfilters import slugify


class User(AbstractUser):
    email = models.EmailField(max_length = 255,unique = True , validators = [fake_email_validation,] )
    username = models.CharField(max_length = 20,unique = True )
    phone = models.CharField(max_length = 10 ,unique = True ,default = "xxxxxxxxx" ,validators = [phone_number_validation,])
    joined = models.DateTimeField(auto_now_add = True)
    is_admin = models.BooleanField(default = False)
    employee = models.BooleanField(default = False)

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['username','phone']

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.phone[0] == '0':
            self.phone = self.phone[1:] # self.value is a model field.
        self.email = self.email.lower()
        super().save(*args, **kwargs)

GENDER = (
    ('MALE',_('MALE')),
    ('FEMALE',_('FEMALE')),
)

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE,unique = True)
    firstName = models.CharField( _('first name'),max_length = 20 , null = True)
    lastName = models.CharField(_('last name'),max_length = 20, null = True)
    meterNumber = models.CharField(max_length = 10 ,unique = True ,validators = [phone_number_validation,])
    gender = models.CharField(_('gender') , choices = GENDER ,max_length = 10, null = True )
    profileImage = models.ImageField(_('profile image'),upload_to = 'usersImages')
    birthday = models.DateField(_('birthday'), null = True )
    address = models.CharField(_('addess'),max_length = 100, null = True )
    profileComplete = models.BooleanField(default ='False')

    def save(self, *args, **kwargs):
        self.meterNumber = self.user.phone
        super().save(*args,**kwargs)

    def __str__(self):  # string representation of the profile when it gets created.
        return slugify(self.user.username + ' Profile')

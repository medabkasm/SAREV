from django.contrib import admin
from .models import User , Profile
# Register your models here.


class UserAdminManager(admin.ModelAdmin):
    search_fields = ['email','username','phone']
    class Meta:
        model = User

class UserRegister(admin.ModelAdmin):
    class Meta:
        model = User
        
class ProfileAdminManager(admin.ModelAdmin):
    search_fields = ['firstName','lastName','user__username','meterNumber','birthday','address']
    class Meta:
        model = Profile




admin.site.register(User , UserAdminManager)  # add the user model to the admin panel.
admin.site.register(Profile , ProfileAdminManager)

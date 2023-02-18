from django.contrib import admin
from .models import Data , Bill
# Register your models here.


class DataAdminManager(admin.ModelAdmin):
    search_fields = ['meterNumber',]
    readonly_fields = ('date',)
    class Meta:
        model = Data

class BillAdminManager(admin.ModelAdmin):
    search_fields = ['id','user__username','user__profile__firstName','user__profile__lastName','power','date']
    readonly_fields = ('id','date',)
    class Meta:
        model = Bill


admin.site.register(Data , DataAdminManager)
admin.site.register(Bill , BillAdminManager)

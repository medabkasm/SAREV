from django.db import models
from accounts.models import *
# Create your models here.



class Data(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    voltage = models.FloatField()
    current = models.FloatField()
    power = models.FloatField()
    date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.user.username + "'s data"


class Bill(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    voltage = models.FloatField(null = True)
    avgCurrent = models.FloatField(null = True)
    power = models.FloatField()
    date = models.DateTimeField(auto_now_add = True)
    payed = models.BooleanField(default ='False')
    amount = models.FloatField()

    def save(self, *args, **kwargs):
        self.amount = self.power * 0.2
        super().save(*args, **kwargs)


    def __str__(self):
        return self.user.username + "'s Bill"

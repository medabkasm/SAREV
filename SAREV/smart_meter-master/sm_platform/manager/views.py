from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from accounts.models import User , Profile
from .models import Data , Bill
from	django.utils.translation	import	gettext_lazy	as	_
from django.contrib import messages
from django.contrib.auth import authenticate
from .decorators import *
from django.core import serializers
import json
from django.http import JsonResponse

# Create your views here.

def add_data(request,distributerName,distributerPass,meterNumber,voltage,current):
    distributer = authenticate(username=distributerName, password=distributerPass)
    if distributer is not None:
        try:
            meter = Profile.objects.get(meterNumber = meterNumber)
            try:
                user = meter.user
                power = float(current) * float(voltage)
                data = Data.objects.create(user = user , voltage = voltage , current = current ,power = power)
                data.save()
            except Exception as err:
                return HttpResponse("ERR - "+str(err),content_type="text/plain")
        except Exception as err:
            return HttpResponse("ERR - "+str(err),content_type="text/plain")

        if (Data.objects.filter(user=user).count() % 6) == 0:
            avgCurrent = 0
            avgVoltage = 0
            for data in Data.objects.filter(user = user).order_by('-id')[:6]:
                power = power + data.power
                avgCurrent = avgCurrent + ( data.current / 6 )
                avgVoltage = avgVoltage + ( data.voltage / 6 )

            try:
                Bill.objects.create(user = user , avgCurrent = avgCurrent,voltage = avgVoltage , power = power)
                return HttpResponse("DONE - BILL CREATED" , content_type = "text/plain")
            except:
                return HttpResponse("ERR - unable to create a Bill",content_type="text/plain")
        return HttpResponse("DONE",content_type="text/plain")

    return HttpResponse("ERR - meter number is not defined",content_type="text/plain")


@login_required
@profile_complete
def get_bill(request,username,id):
    print(username,id)
    avgCurrent = 0
    if request.user.username == username:
        try:
            bill = Bill.objects.get(id=id)
            if bill:
                return render(request,'manager/bil.html',{'bill':bill})
            else:
                message = _("unable to find the bill with id of {}".format(id))
                messages.warning(request,message)
                return redirect("profiles:profile",request.user.username)

        except Exception as err:
            print(str(err))
            message = _("trouble with finding the bill with id of {}".format(id))
            messages.warning(request,message)

    return redirect("profiles:profile",request.user.username)


@login_required
@profile_complete
def dash_board(request,username):
    if request.user.username == username :
        try:
            bills = Bill.objects.filter(user = request.user).order_by('-id')
        except:
            bills = None
            data = None
        return render(request,"manager/dash_board.html",{'bills':bills})

    return redirect("profiles:profile",request.user.username)



@login_required
@profile_complete
def ajax_chart(request):
    if request.is_ajax():
        powerList = []
        dateList = []
        currentList = []
        datas = Data.objects.filter(user = request.user)
        if datas:
            for data in datas:
                powerList.append(data.power)
                dateList.append(data.date.date())
                currentList.append(data.current)

            return JsonResponse({'power':powerList,'current' : currentList,'date':dateList},safe=False,status = 200)

        return JsonResponse(None,safe=False,status = 400)



@login_required
@profile_complete
def ajax_bills(request):
    if request.is_ajax() :
        idList = []
        powerList = []
        currentList = []
        voltageList = []
        dateList = []
        currentList = []
        amountList = []
        datas = Bills.objects.filter(user = request.user)
        if(datas):
            for data in datas:
                idList.append(data.id)
                powerList.append(data.power)
                dateList.append(data.date.date())
                currentList.append(data.avgCurrent)
                voltageList.append(data.avgVoltage)
                amountList.append(data.amount)

            return JsonResponse({'id':idList,'power':powerList,'current' : currentList,'voltage' : voltageList,'amount': amountList,'date':dateList},safe=False,status = 200)

        return JsonResponse(None,safe=False,status = 400)


@login_required
@profile_complete
def ajax_bills_emp(request):
    if request.is_ajax() and (request.user.employee or request.user.is_admin):
        billsList = []
        billDict = {}
        try:
            bills = Bill.objects.filter(payed = False)
            for bill in bills:
                billDict['id'] = bill.id
                billDict['username'] = bill.user.username
                billDict['power'] = bill.power
                billDict['amount'] = bill.amount
                billDict['date'] = bill.date
                billDict['payed'] = bill.payed
                billsList.append(billDict.copy())
            return JsonResponse({'bills':billsList},safe=False,status = 200)
        except:
            return JsonResponse(None,safe=False,status = 200)
    return JsonResponse(None,safe=False,status = 400)


@login_required
@profile_complete
def ajax_user(request):
    if request.is_ajax() and (request.user.employee or request.user.is_admin):
        usersList = []
        userDict = {}
        phone = request.GET.get('phone', None)
        if phone:
            try:
                user = User.objects.get(phone = phone)
                userDict['username'] = user.username
                userDict['phone'] = user.phone
                userDict['email'] = user.email
                userDict['joined'] = user.joined
                usersList.append(userDict.copy())
                return JsonResponse({'users':usersList},safe=False,status = 200)
            except:
                return JsonResponse(None,safe=False,status = 200)
        return JsonResponse(None,safe=False,status = 200)

    return JsonResponse(None,safe=False,status = 400)

@login_required
@profile_complete
def ajax_users(request):
    if request.is_ajax() and (request.user.employee or request.user.is_admin):
        usersList = []
        userDict = {}
        try:
            profiles = Profile.objects.filter(profileComplete = False)
            for profile in profiles:
                userDict['id'] = profile.user.id
                userDict['username'] = profile.user.username
                userDict['phone'] = profile.user.phone
                userDict['email'] = profile.user.email
                userDict['joined'] = profile.user.joined
                userDict['profileComplete'] = profile.profileComplete
                usersList.append(userDict.copy())
            return JsonResponse({'users':usersList},safe=False,status = 200)
        except:
            return JsonResponse(None,safe=False,status = 200)
    return JsonResponse(None,safe=False,status = 400)


@login_required
@profile_complete
def check_user(request,username):
    if request.user.is_admin or request.user.employee:
        try:
            user = Profile.objects.get(user__username = username)
            if user:
                user.profileComplete = True
                user.save()
                message = _("Profile with username - {} - confirmed".format(username))
                messages.success(request,message)
                return redirect('manager:dash_board',request.user.username)
        except:
            message = _("Unable to confirm profile with username - {} -".format(username))
            messages.warning(request,message)
            return redirect('manager:dash_board',request.user.username)
    return redirect('profiles:profile',request.user.username)

@login_required
@profile_complete
def check_bill(request,id):
    if request.user.is_admin or request.user.employee:
        try:
            bill = Bill.objects.get(id = id)
            if bill:
                bill.payed = True
                bill.save()
                message = _("Bill with id number - {} - marked as payed".format(id))
                messages.success(request,message)
                return redirect('manager:dash_board',request.user.username)
        except:
            message = _("Unable to mark the Bill with id number - {} - as payed".format(id))
            messages.warning(request,message)
            return redirect('manager:dash_board',request.user.username)
    return redirect('profiles:profile',request.user.username)


@login_required
@profile_complete
def user_bill(request,id):
    if request.user.is_admin or request.user.employee:
        try:
            bill = Bill.objects.get(id = id)
            if bill:
                if bill.payed:
                    message = _("Bill with id number - {} - is already payed".format(id))
                    messages.warning(request,message)
                    return redirect('manager:dash_board',request.user.username)
                return render(request,'manager/user_bill.html',{'bill':bill})
            else:
                message = _("Unable to get the Bill with id number - {} -".format(id))
                messages.warning(request,message)
                return redirect('manager:dash_board',request.user.username)
        except:
            message = _("Unable to get the Bill with id number - {} -".format(id))
            messages.warning(request,message)
            return redirect('manager:dash_board',request.user.username)

    return redirect('profiles:profile',request.user.username)

@login_required
@profile_complete
def user_profile(request,username):
    if request.user.is_admin or request.user.employee:
        try:
            user = User.objects.get(username = username)
            if user and user.profile:
                if user.profile.profileComplete:
                    message = _("Profile with username - {} - is already completed".format(username))
                    messages.warning(request,message)
                    return redirect('manager:dash_board',request.user.username)
                return render(request,'manager/user_profile.html',{'user':user,'this_user':request.user})
            else:
                message = _("Unable to get user profile with username - {} -".format(username))
                messages.warning(request,message)
                return redirect('manager:dash_board',request.user.username)
        except:
            message = _("Unable to get user profile with username - {} -".format(username))
            messages.warning(request,message)
            return redirect('manager:dash_board',request.user.username)

    return redirect('profiles:profile',request.user.username)

from .forms import CreateUserForms
from .models import *
import json, datetime as dt
from dateutil.relativedelta import *
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test 

#Возвращает True если подписка есть
def user_is_subscribed(user):
    if user:
        try:
            sub = UserSub.objects.get(user=user)
            if dt.datetime.now().date() <= sub.date_end:
                return True
            else:
                return False 
        except UserSub.DoesNotExist:
            return False
    return False

#Возвращает True если нет подписки
def user_without_sub(user):
    if user:
        try:
            sub = UserSub.objects.get(user=user)
            return False 
        except UserSub.DoesNotExist:
            return True
    return False

# Create your views here.
def userMain(request):
    return redirect('login')


def userLogin(request):
    if request.user.is_authenticated:
        if user_is_subscribed(request.user):
            return redirect('table')
        else:
            return redirect('choicesub')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('choicesub')
            else:
                messages.info(request, 'Логин или пароль неправильный!')

        return render(request, 'loggining/login.html')


@login_required(login_url='index')
def userLogout(request):
    logout(request)
    return redirect('index')


def userRegister(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form = CreateUserForms()
        if request.method == 'POST':
            form = CreateUserForms(request.POST)
            if form.is_valid():
                form.save()
                name = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                user = authenticate(request, username=name, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('choicesub')
                else:
                    return redirect('login')            

    context = {'form':form} 
    return render(request, 'loggining/register.html', context)


def userResetpswd(request):
    pass


@login_required(login_url='login')
@user_passes_test(user_without_sub, login_url='table', redirect_field_name=None)
def userChoiseSub(request):
    if request.method == 'POST':
        current_user = request.user
        subname = request.POST.get('selectsub')
        sub = Subscription.objects.get(name=subname)
        start = dt.datetime.now()
        end = start+relativedelta(months=+sub.period)
        if user_without_sub(current_user):
            userSub = UserSub(user=current_user, sub_id=sub, date_start=start, date_end=end)
            userSub.save()
            return redirect('table')
    
    subs = Subscription.objects.all()
    context = {'Subs': subs}

    return render(request, 'loggining/choicesub.html', context)
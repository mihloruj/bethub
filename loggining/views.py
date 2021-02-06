from .forms import CreateUserForms, UserChangePassword
from .models import *
import json, datetime as dt
from dateutil.relativedelta import *
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test 

from .sub_services import *


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
                if user_is_subscribed(user):
                    return redirect('table')
                else:
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
        return redirect('table')
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


@login_required(login_url='login')
def userProfile(request):
    user = request.user
    data = get_info_about_sub(user)
    
    if request.method == 'POST':
        form = UserChangePassword(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Пароль успешно изменен!')
            return redirect('profile')
        else:
            messages.error(request, 'Введенные данные некорректны')
            return redirect('profile')
    else:
        form = UserChangePassword(request.user)

    return render(request, 'loggining/profile.html', context={
        "data": data,
        "form": form })


@login_required(login_url='login')
@user_passes_test(user_sub_end, login_url='resub', redirect_field_name=None)
@user_passes_test(user_without_sub, login_url='table', redirect_field_name=None)
def userChoiseSub(request):
    if request.method == 'POST':
        current_user = request.user
        subname = request.POST.get('selectsub')
        sub = Subscription.objects.get(name=subname)
        start = dt.datetime.now().date()
        end = start+relativedelta(months=+sub.period)
        if user_without_sub(current_user):
            userSub = UserSub(user=current_user, sub_id=sub, date_start=start, date_end=end)
            userSub.save()
            return redirect('table')
    
    subs = Subscription.objects.all()
    context = {'Subs': subs}

    return render(request, 'loggining/choicesub.html', context)


@login_required(login_url='login')
@user_passes_test(user_with_sub, login_url='choicesub', redirect_field_name=None)
def userReSub(request):
    if request.method == 'POST':
        current_user = request.user
        subname = request.POST.get('selectsub')
        sub = Subscription.objects.get(name=subname)
        user_sub = UserSub.objects.get(user=current_user)
        now = dt.datetime.now().date()
        if now <= user_sub.date_end:
            start = user_sub.date_end
        else:
            start = now
        end = start+relativedelta(months=+sub.period)
        user_sub.date_end = end
        user_sub.save()
        return redirect('table')
    
    subs = Subscription.objects.all()
    context = {'Subs': subs}

    return render(request, 'loggining/prolongationsub.html', context)
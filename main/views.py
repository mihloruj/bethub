import json, datetime as dt
from loggining.models import UserSub
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test


from .table_services import getStatResponse, getMatches, getLastMatches, getLastMatchesByLigname
from .next_services import getMatchesNext, getOldMatchesNext
from .leagues import LEAGUES


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


def index(request):
    return render(request, 'main/index.html')


@login_required(login_url='login')
@user_passes_test(user_is_subscribed, login_url='choicesub', redirect_field_name=None)
def mainTable(request):
    return render(request, 'main/table.html')


@login_required(login_url='login')
@user_passes_test(user_is_subscribed, login_url='choicesub', redirect_field_name=None)
def mainNext(request):
    return render(request, 'main/next.html')



@login_required(login_url='login')
@user_passes_test(user_is_subscribed, login_url='choicesub', redirect_field_name=None)
def mainListLeagues(request):
    return render(request, 'main/leagues.html', context = {
        'leagues': LEAGUES
    })


# @login_required(login_url='login')
# @user_passes_test(user_is_subscribed, login_url='choicesub', redirect_field_name=None)
# def mainProfile(request):
#     user = request.user
#     userInfo = User.objects.get(id=user.id)
#     subInfo = UserSub.objects.get(user=user)
#     data = {
#         "id": userInfo.id,
#         "name": userInfo.username,
#         "email": userInfo.email,
#         "endtime": subInfo.date_end
#     }
    
#     if request.method == 'POST':
#         form = UserChangePassword(request.user, request.POST)
#         if form.is_valid():
#             form.save()
#             update_session_auth_hash(request, form.user)
#             messages.success(request, 'Пароль успешно изменен!')
#             return redirect('profile')
#         else:
#             messages.error(request, 'Введенные данные некорректны')
#             return redirect('profile')
#     else:
#         form = UserChangePassword(request.user)

#     return render(request, 'main/profile.html', context={
#         "data": data,
#         "form": form })


#
#   Функции обработки AJAX-запросов 
#

# Получение матчей для основной таблицы
@login_required(login_url='login')
@user_passes_test(user_is_subscribed, login_url='choicesub', redirect_field_name=None)
def ajaxTableMatches(request):
    if request.is_ajax and request.method == "GET":
        coef_p1 = request.GET.get("p1", None)
        coef_x  = request.GET.get("x", None)
        coef_p2 = request.GET.get("p2", None)
        ligname = request.GET.get("ligname", None)
        country = request.GET.get("country", None)
        #and country == 'Все континенты'
        if coef_p1 == '' and coef_p2 == '' and coef_x == '' and ligname == '' or country == None:
            matches = getLastMatches(country)
        elif coef_p1 == '' and coef_p2 == '' and coef_x == '' or country == None:
            matches = getLastMatchesByLigname(country, ligname)
        else:    
            matches = getMatches(coef_p1, coef_x, coef_p2, ligname, country)
        matches_list = serializers.serialize('json', matches)
        answer = []
        for j in json.loads(matches_list):
            answer.append(j['fields'])
        return JsonResponse({'data': answer}, status=200)
    return JsonResponse({}, status = 400)


# Получение статистики по коридору
@login_required(login_url='login')
@user_passes_test(user_is_subscribed, login_url='choicesub', redirect_field_name=None)
def ajaxStatMatch(request):
    if request.is_ajax and request.method == "GET":
        coef_p1 = request.GET.get("p1", None)
        coef_x  = request.GET.get("x", None)
        coef_p2 = request.GET.get("p2", None)
        ligname = request.GET.get("ligname", None)
        country = request.GET.get("country", None)

        if coef_p1 == '' and coef_p2 == '' and coef_x == '' and country != '':
            return JsonResponse({"valid":False}, status = 200)
        else:
            return JsonResponse(getStatResponse(coef_p1, coef_x, coef_p2, ligname, country), status = 200)

    return JsonResponse({}, status = 400)


# Получение матчей для линии на сегодня
@login_required(login_url='login')
@user_passes_test(user_is_subscribed, login_url='choicesub', redirect_field_name=None)
def ajaxNextMatches(request, old):
    if request.is_ajax and request.method == "GET":
        if old == 1:
            m = getOldMatchesNext()
        else:
            m = getMatchesNext()
        matches_list = serializers.serialize('json', m)
        answer = []
        for j in json.loads(matches_list):
            answer.append(j['fields'])
        return JsonResponse({'data': answer}, status=200)    
    return JsonResponse({}, status = 400)

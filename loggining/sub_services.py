from .models import Subscription, UserSub, User
import json, datetime as dt


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


#Возвращает False если подписка есть или закончилась
def user_sub_end(user):
    try:
        sub = UserSub.objects.get(user=user)
        if sub:
            return False
        else:
            return True 
    except UserSub.DoesNotExist:
        return True


#Возвращает False подписка есть или была
def user_without_sub(user):
    try:
        sub = UserSub.objects.get(user=user)
        return False
    except UserSub.DoesNotExist:
        return True


#Возвращает False если нет подписки
def user_with_sub(user):
    try:
        sub = UserSub.objects.get(user=user)
        return True
    except UserSub.DoesNotExist:
        return False


def get_info_about_sub(user):
    userInfo = User.objects.get(id=user.id)
    try:
        subInfo = UserSub.objects.get(user=user)
        return {
                "id": userInfo.id,
                "name": userInfo.username,
                "email": userInfo.email,
                "endtime": subInfo.date_end,
                "type": 'Стандартная',
                "isSub": True
            }
    except:
        msg = 'Вы еще не оформили подписку'
        return {
                "id": userInfo.id,
                "name": userInfo.username,
                "email": userInfo.email,
                "endtime": msg,
                "type": msg,
                "isSub": False
            }
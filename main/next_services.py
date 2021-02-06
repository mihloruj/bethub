from .models import NextMatch
import datetime as dt


def getMatchesNext():
    return NextMatch.objects.filter(old=False).order_by('id')


def getOldMatchesNext():
    return NextMatch.objects.filter(old=True).order_by('id')
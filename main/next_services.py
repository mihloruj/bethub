from .models import NextMatch
import datetime as dt


def getMatchesNext():
    # Этот способ будет актуален при указании дата+время, иначе обрезается ночь
    # time2h = dt.datetime.strftime( dt.datetime.now() - dt.timedelta(hours=2) , '%H:%M')
    # print(time2h)
    # return NextMatch.objects.filter(time__gte=time2h).order_by('id')
    return NextMatch.objects.all().order_by('id')

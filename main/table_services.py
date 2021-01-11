from .models import Match
from .leagues import LEAGUES

# Из одного кэфа формирует минимальный и максимальный - 1.57 -> 1.5 и 1.6
def normalizeCoef(coef):
    coef_min = int(float(coef)* 10) / 10
    coef_max = round((coef_min + 0.09), 1)
    return coef_min, coef_max


# Считает минимальный и максимальный кэф на основе необработанного кэфа  
def getMinMaxCoefs(coef):
    if coef != '' and coef != None:
        return normalizeCoef(coef) 
    else:
        return 0, 100


# Считает кол-во исходов П1 Х П2 на основе коллекции матчей
def getWinsCount(matches):
    countP1 = 0
    countX  = 0
    countP2 = 0
    for match in matches:
        s1 = int(match.total_score.split(':')[0])
        s2 = int(match.total_score.split(':')[1].split(' ')[0])
        if s1 > s2:
            countP1+=1
        elif s2 > s1:
            countP2+=1
        elif s1 == s2:
            countX+=1
    return countP1, countX, countP2


# Считает процент исхода
def getPercentWin(countWin, count):
    return round((100 / count * countWin), 1)


# Считает профит коридора по кэфу
def getProfit(coef, countWin, count):
    if coef != 0:
        return round((coef - 1) * countWin - (count - countWin) , 2)
    else:
        return '-'


# Получение коллекции лиг по континенту
def getSelectedLeagues(country):
    return LEAGUES[country]


def getAdvanceStat(matches, count):
    tb25=tm25=oz=p1p1=xp1=p2p1=p1x=p2x=p1p2=xp2=p2p2=xx = 0
    for match in matches:
        r1 = int(match.total_score.split(':')[0])
        r2 = int(match.total_score.split(':')[1].split(' ')[0])
        r1_t = int(match.first_half_score.split(':')[0])
        r2_t = int(match.first_half_score.split(':')[1])

        p1=p2=n=p1_t=p2_t=n_t=False

        if r1 > r2:
            p1 = True
        if r2 > r1:
            p2 = True
        if r1 == r2:
            n = True
        if r1_t > r2_t:
            p1_t = True
        if r2_t > r1_t:
            p2_t = True
        if r1_t == r2_t:
            n_t = True
        if r1 + r2 >= 3:
            tb25+=1
        if r1 + r2 < 3:
            tm25+=1
        if r1 > 0 and r2 > 0:
            oz+=1
        if p1_t and p1:
            p1p1+=1 
        if n_t and p1:
            xp1+=1 
        if p2_t and p1:
            p2p1+=1 
        if p1_t and n:
            p1x+=1 
        if p2_t and n:
            p2x+=1 
        if p1_t and p2:
            p1p2+=1 
        if n_t and p2:
            xp2+=1 
        if p2_t and p2:
            p2p2+=1 
        if n_t and n:
            xx+=1
    return {
        "tb25": round((tb25/count*100), 1),
        "tm25": round((tm25/count*100), 1),
        "oz": round((oz/count*100), 1),
        "p1p1": round((p1p1/count*100), 1),
        "xp1": round((xp1/count*100), 1),
        "p2p1": round((p2p1/count*100), 1),
        "p1x": round((p1x/count*100), 1),
        "p2x": round((p2x/count*100), 1),
        "p1p2": round((p1p2/count*100), 1),
        "xp2": round((xp2/count*100), 1),
        "p2p2": round((p2p2/count*100), 1),
        "xx": round((xx/count*100), 1) 
    }
    

# Возвращает отфильтрованную коллекцию матчей 'K < K_max AND K >= K_min AND lname LIKE liga*'  
def getMatchesWithCountry(p1, x, p2, p1_max, x_max, p2_max, liga, country):
    return Match.objects.filter(coef_p1__lt=p1_max, coef_p1__gte=p1, 
                                coef_x__lt=x_max, coef_x__gte=x,
                                coef_p2__lt=p2_max, coef_p2__gte=p2, 
                                league_name__istartswith=liga,
                                league_name__in = getSelectedLeagues(country)).order_by('-id')


def getMatchesWithoutCountry(p1, x, p2, p1_max, x_max, p2_max, liga):
    return Match.objects.filter(coef_p1__lt=p1_max, coef_p1__gte=p1, 
                                coef_x__lt=x_max, coef_x__gte=x,
                                coef_p2__lt=p2_max, coef_p2__gte=p2, 
                                league_name__istartswith=liga).order_by('-id')


def getMatches(coefP1, coefX, coefP2, leagueName, country):
    p1, p1_max = getMinMaxCoefs(coefP1)
    x , x_max  = getMinMaxCoefs(coefX)
    p2, p2_max = getMinMaxCoefs(coefP2)
    
    if country == 'Все континенты':
        return getMatchesWithoutCountry(p1, x, p2, p1_max, x_max, p2_max, leagueName)
    else:
        return getMatchesWithCountry(p1, x, p2, p1_max, x_max, p2_max, leagueName, country)


def getLastMatches(country):
    if country == 'Все континенты' or country == None:
        return Match.objects.all().order_by('-id')[:10:1]
    else:
        return Match.objects.filter(league_name__in = getSelectedLeagues(country)).order_by('-id')[:10:1]
    

# Формирует статистику коллекции матчей на основе всех фильтров
def getStatResponse(coefP1, coefX, coefP2, leagueName, country):
    p1, p1_max = getMinMaxCoefs(coefP1)
    x , x_max  = getMinMaxCoefs(coefX)
    p2, p2_max = getMinMaxCoefs(coefP2)

    if country == 'Все континенты':
        matches = getMatchesWithoutCountry(p1, x, p2, p1_max, x_max, p2_max, leagueName)
    else:
        matches = getMatchesWithCountry(p1, x, p2, p1_max, x_max, p2_max, leagueName, country)
    countMatches = len(matches)

    if countMatches > 0:
        countP1, countX, countP2 = getWinsCount(matches)
        percentP1 = getPercentWin(countP1, countMatches)
        percentX  = getPercentWin(countX , countMatches)
        percentP2 = getPercentWin(countP2, countMatches)
        profitP1  = getProfit(p1, countP1, countMatches)
        profitX   = getProfit(x , countX , countMatches)
        profitP2  = getProfit(p2, countP2, countMatches)
        return {'valid'    : True,
                'count'    : countMatches,
                'countW1'  : countP1,
                'countN'   : countX,
                'countW2'  : countP2,
                'percentW1': percentP1,
                'percentN' : percentX,
                'percentW2': percentP2,
                'fltP1'    : profitP1,
                'fltX'     : profitX,
                'fltP2'    : profitP2,
                'advanced' : getAdvanceStat(matches, countMatches)
            }
    else:
        return {'valid'    : False}











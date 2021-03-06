import requests, json, psycopg2
from multiprocessing import Pool
import datetime as dt
from bs4 import BeautifulSoup

from settings import *


# Формирование строки с названием пари в формате 'КОМАНДА1 - КОМАНДА2' из двух разных спанов
def getMatchName(a):
    spans = a.find_all('span')
    names = []
    for span in spans:
        if span.find('strong') is not None: 
            names.append(span.find('strong').text)
        else:
            names.append(span.text)
    return '%s - %s' % (names[0], names[1])


# Все матчи приходят с временем +1 час: метод возвращет время в формате +3
def getCorrectTime(time):
    return (dt.datetime.strptime(time, '%H:%M') + dt.timedelta(hours=2)).strftime('%H:%M')


#   ---Основная функция---
# Получает страницу с матчами и выдергивает html
# Парсит каждый матч и достает о нем нужную информацию:
# ссылка, лига, название пари, время матча 
def getAllInfoAboutNextMatches(url):
    response = requests.get(url, headers=HEADERS ,timeout=5)
    if response.status_code == 200:
        matches = []
        html = BeautifulSoup(response.text, 'html.parser')
        all_tbody = html.find_all('tbody')
        last_date = dt.datetime.now().date()
        stop = False
        time_end = '02:00'
        for body in all_tbody:
            if not stop:
                all_tr = body.find_all('tr', attrs={'data-def': 1})
                match_liga = body.find('a', 'table-main__tournament').text
                for tr in all_tr:
                    try:
                        match_date = dt.datetime.strptime('-'.join(tr['data-dt'].split(',')[:-2]), '%d-%m-%Y').date()
                        match_link = BASE_SITE_URL+tr.find('a')['href']
                        match_name = getMatchName(tr.find('a'))
                        match_time = getCorrectTime(tr.find('span', 'table-main__time').text)
                        result = {
                            "link": match_link,
                            "name": match_name,
                            "liga": match_liga,
                            "time": match_time
                        }
                        if (match_date == last_date and match_time != time_end):
                            matches.append(result)
                            print(match_date, match_name, match_time)
                        elif (match_date != last_date and match_time == time_end):
                            matches.append(result)
                            print(match_date, match_name, match_time)
                        elif (match_date != last_date and match_time != time_end):
                            stop = True
                            break
                    except Exception as e:
                        print(e)
            else:
                break
        return matches
    else:
        print('ERROR: page is not available, code', response.status_code)
        return None


# Удаляет все предыдущие записи и загружает информацию о матчах на сегодня 
def pullDataToDB(data):
    try:
        connection = psycopg2.connect(  user = DB_USER,
                                        password = DB_PASSWORD,
                                        host = DB_HOST,
                                        port = DB_PORT,
                                        database = DB_NAME)
        print("INFO: connection is opened")
        if data != None:
            cursor = connection.cursor()
            cursor.execute('DELETE FROM main_nextmatch WHERE old is true;')
            print('DALETE ROWS IN TABLE main_nextmatch')
            cursor.execute('UPDATE main_nextmatch SET old = TRUE;')
            print('UPDATE ROWS IN TABLE main_nextmatch')
            for d in data:
                cursor.execute('INSERT INTO main_nextmatch(url, league_name, match_name, time, old) VALUES (%s,%s,%s,%s, false);', 
                (d['link'],d['liga'],d['name'],d['time']))
            connection.commit()
            print('INSERT INTO main_nextmatch', len(data), 'ROWS')
            print("INFO: data loaded successfully")
    except (Exception, psycopg2.Error) as error :
        print ("ERROR: error while connecting to PostgreSQL", error)
    finally:
            if(connection):
                cursor.close()
                connection.close()
                print("INFO: connection is closed")


if __name__ == "__main__":
    print('\nINFO: start script', str(dt.datetime.now().date()))
    start = dt.datetime.now()
    
    data = getAllInfoAboutNextMatches('https://www.betexplorer.com/next/soccer/')
    pullDataToDB(data)
    total = dt.datetime.now() - start
    print('INFO: end script, total run time:',str(total))
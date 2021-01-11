import requests, json, psycopg2
from multiprocessing import Pool
from psycopg2.extras import DictCursor
import datetime as dt, time
from bs4 import BeautifulSoup
import os

from settings import *

FILENAME = 'results_next_matches_%s.csv' % str(dt.datetime.now())
FILENAME_B = 'bad_next_matches_%s.csv' % str(dt.datetime.now())


# Достаем данные из файла, куда сложили работу воркеры, после удаляем файл
def getDataFromFile(file):
    try:
        with open(file) as f:
            s = f.read()[:-1]
            s = str('[' + s[:-1] + ']') 
            data = json.loads(s)
        os.remove(file)
        return data
    except Exception as e:
        print('ERROR: load data from file is failed', e)
        return None


# Получаем матчи из таблицы, время начала которых ровно текущему времени 
def getMatchesFromDB():
    try:
        connection = psycopg2.connect(  user = DB_USER,
                                        password = DB_PASSWORD,
                                        host = DB_HOST,
                                        port = DB_PORT,
                                        database = DB_NAME)
        print("INFO: connection is opened")
        curDate = dt.datetime.now().strftime('%H:%M')
        cursor = connection.cursor(cursor_factory=DictCursor)
        cursor.execute('SELECT * FROM main_nextmatch where time = %s;', (curDate, ))
        records = cursor.fetchall()
        connection.commit()
        print('SELECTED', len(records))
        print("INFO: data selected successfully")
    except (Exception, psycopg2.Error) as error :
        print ("ERROR: error while connecting to PostgreSQL", error)
        return None
    finally:
            if(connection):
                cursor.close()
                connection.close()
                print("INFO: connection is closed")
                return records


# Обновляем записи в базе, у которых получены кэфы
def updateDataInDB():
    try:
        connection = psycopg2.connect(  user = DB_USER,
                                        password = DB_PASSWORD,
                                        host = DB_HOST,
                                        port = DB_PORT,
                                        database = DB_NAME)
        print("INFO: connection is opened")
        data = getDataFromFile(FILENAME)
        data_b = getDataFromFile(FILENAME_B)
        cursor = connection.cursor()
        if data is not None:
            for d in data:
                cursor.execute('UPDATE main_nextmatch SET coef_p1 = %s , coef_x = %s, coef_p2 = %s WHERE id = %s;', 
                (d['p1'],d['x'],d['p2'],d['id']))
            connection.commit()
            print('UPDATE', len(data)) 
            print("INFO: data loaded successfully")
        if data_b is not None:
            for d in data_b:
                cursor.execute('DELETE FROM main_nextmatch WHERE id = %s;', 
                (d['id'],))
            connection.commit()
            print('DELETE', len(data_b)) 
            print("INFO: bad matches deleted successfully")
    except (Exception, psycopg2.Error) as error :
        print ("ERROR: error while connecting to PostgreSQL", error)
    finally:
            if(connection):
                cursor.close()
                connection.close()
                print("INFO: connection is closed")
    

# Пробуем получить кэфы матча, если удается - складываем данные в файл, если нет - матч хуйня
def getResult(match):
    try:
        link = match[1]
        id = match[0]
        idMatch = link.replace('/', ' ').split(' ')[-2]
        url = 'https://www.betexplorer.com/match-odds/%s/0/1x2/' % idMatch
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            response = response.text.replace("\\", "")
            soup = BeautifulSoup(response, 'html.parser')
            td = soup.find_all('td', {'data-bid':'18'})
            res = []
            for t in td:
                res.append(str(t).replace('=', ' ').split('data-odd')[1].split(' ')[1].replace('"', ''))
            data = {
                "p1": res[0],
                "x": res[1],
                "p2": res[2],
                "link": link,
                "id": id
            }
            dataJson = json.dumps(data)
            with open(FILENAME, 'a') as output_file:
                output_file.write(str(dataJson)+',\n')
            print('INFO: result OK, link', link)
        else:
            print('ERROR: it is impossible to get the result, the page is not available, code', response.status_code)
    except Exception as e:
        bad_match_data = {
            "id": id
        }
        dataJson = json.dumps(bad_match_data)
        with open(FILENAME_B, 'a') as output_file:
            output_file.write(str(dataJson)+',\n')
        print('SKIP: match is huinya', link, e ) 


if __name__ == "__main__":
    curDate = dt.datetime.now()
    print('\nINFO: start script', str(curDate.date()))
    print('INFO: current time: ',curDate.strftime('%H:%M'))
    start = curDate

    upcomingNextMatches = getMatchesFromDB()
    if upcomingNextMatches is not None and len(upcomingNextMatches) > 0:
        time.sleep(5)
        with Pool(10) as p:
            p.map(getResult, upcomingNextMatches)
        updateDataInDB()
    else:
        print("INFO: upcoming matches not found")

    total = dt.datetime.now() - start
    print('INFO: end script, total run time:',str(total))

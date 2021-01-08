import requests, json, psycopg2
import datetime as dt
from multiprocessing import Pool
from bs4 import BeautifulSoup

from settings import *


FILENAME = 'results_%s.csv' % str(dt.datetime.now().date())


def getAllLinks(url):
    response = requests.get(url, headers=HEADERS ,timeout=5)
    if response.status_code == 200:
        all_links = []
        soup = BeautifulSoup(response.text, 'html.parser')
        all_tbody = soup.find_all('tbody')
        for body in all_tbody:
            tr = body.find_all('tr', attrs={'data-def': 1})
            for r in tr:
                all_links.append(BASE_SITE_URL+r.find('a')['href'])
        return all_links
    else:
        print('ERROR: page is not available, code', response.status_code)
        return None


def getDataMatch(link):
    response = requests.get(link, headers=HEADERS).text
    soup = BeautifulSoup(response, 'html.parser')
    liga_name = soup.find('h1', 'wrap-section__header__title').find('a').get_text()
    match_name = soup.find('span', 'list-breadcrumb__item__in').get_text()
    date = str(soup.find('p', 'list-details__item__date').get('data-dt')).split(',')
    match_date = '-'.join(date[0:3])
    match_time = ':'.join(date[3:5])
    match_score = soup.find('p', 'list-details__item__score').get_text()
    match_score_fh = soup.find('h2', 'list-details__item__partial').get_text().split(',')[0].replace('(', '')
    if match_score_fh.strip() != '':
        data = {
            "liga_name": liga_name,
            "match_name": match_name,
            "match_date": match_date,
            "match_time": match_time,
            "match_score": match_score,
            "match_score_fh": match_score_fh
        }
        return data
    else:
        return None


def getResult(link):
    try:
        idMatch = link.replace('/', ' ').split(' ')[-2]
        url = 'https://www.betexplorer.com/match-odds/%s/1/1x2/' % idMatch
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
                "link": link
            }

            dataMatch = getDataMatch(link)
            if dataMatch != None:
                datafull = {**data, **dataMatch}
                datafull = json.dumps(datafull)
                with open(FILENAME, 'a') as output_file:
                    output_file.write(str(datafull)+',\n')
                print('INFO: result OK, link', link)
            else:
                print('SKIP: dataMatch is bad, link', link)
        else:
            print('ERROR: it is impossible to get the result, the page is not available, code', response.status_code)
    except Exception as e:
        print('SKIP: match is huinya', link, e )


def getDataFromFile():
    try:
        with open(FILENAME) as f:
            s = f.read()[:-1]
            s = str('[' + s[:-1] + ']') 
            data = json.loads(s)
        return data
    except Exception as e:
        print('ERROR: load data from file is failed', e)
        return None
    


def pullDataToDB():
    try:
        connection = psycopg2.connect(  user = DB_USER,
                                        password = DB_PASSWORD,
                                        host = DB_HOST,
                                        port = DB_PORT,
                                        database = DB_NAME)
        print("INFO: connection is opened")
        data = getDataFromFile()
        print(len(data))
        if data != None:
            cursor = connection.cursor()
            for d in data:
                cursor.execute('INSERT INTO matches_history(match_link, liga_name, match_name, match_date, match_time, match_score, match_score_fh, c_p1, c_x, c_p2) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);', 
                (d['link'],d['liga_name'],d['match_name'],d['match_date'],d['match_time'],d['match_score'],d['match_score_fh'],d['p1'],d['x'],d['p2']))
            connection.commit()
            print("INFO: data loaded successfully")
    except (Exception, psycopg2.Error) as error :
        print ("ERROR: error while connecting to PostgreSQL", error)
    finally:
            if(connection):
                cursor.close()
                connection.close()
                print("INFO: connection is closed")


if __name__ == "__main__":
    print('INFO: start script', str(dt.datetime.now().date()))
    start = dt.datetime.now()
    links = getAllLinks('https://www.betexplorer.com/results/soccer/')
    if links != None and len(links) > 0:
        with Pool(10) as p:
            p.map(getResult, links)
        pullDataToDB()
    else:
        print("INFO: results of matches not found")
    end = dt.datetime.now()
    total = end - start
    print('INFO: end script, total run time:',str(total))
import requests, json, psycopg2, os
import datetime as dt
import json, time
import pandas as pd
from multiprocessing import Pool
from bs4 import BeautifulSoup

from settings import *


FILENAME = 'results_%s.csv' % str(dt.datetime.now().date())


def getAllLinks(url):
    response = requests.get(url, headers=HEADERS ,timeout=10)
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


def normalizeLeagueName(name):
    ex = [
        '2021/2022',
        '2020/2021',
        '2019/2020',
        '2018/2019',
        '2017/2018',
        '2022',
        '2021',
        '2020',
        '2019',
        '2018',
        '2017',
        '/'
    ]
    for e in ex:
        name = name.replace(e, '')
    return name.strip()


def getDataMatch(link):
    response = requests.get(link, headers=HEADERS).text
    soup = BeautifulSoup(response, 'html.parser')
    elements = soup.find_all('a', attrs={'class':'list-breadcrumb__item__in'})
    liga_name = elements[-2].text+':'+elements[-1].text
    liga_name = normalizeLeagueName(liga_name)
    match_name = soup.find('span', 'list-breadcrumb__item__in').get_text()
    d = str(soup.find('p', 'list-details__item__date').get('data-dt')).split(',')
    date = dt.date(int(d[2]), int(d[1]), int(d[0])).strftime("%d.%m.%Y")
    match_date = date
    match_score = soup.find('p', 'list-details__item__score').get_text()
    match_score_fh = soup.find('h2', 'list-details__item__partial').get_text().split(',')[0].replace('(', '')
    if match_score_fh.strip() != '':
        data = {
            "link": link,
            "liga_name": liga_name,
            "match_name": match_name,
            "match_date": match_date,
            "match_score": match_score,
            "match_score_fh": match_score_fh
        }
        return data
    else:
        return None


def getCoef1x2(idMatch):
    try:
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
            }
            return data
    except:
        return None


def getCoefOU(idMatch):
    try:
        url = 'https://www.betexplorer.com/match-odds/%s/1/ou/' % idMatch
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            response = response.text.replace("\\", "")
            soup = BeautifulSoup(response, 'html.parser')
            table = soup.find('table', {'id':'sortable-6'})
            td = table.find_all('td', {'data-bid':'18'})
            res = []
            for t in td:
                res.append(str(t).replace('=', ' ').split('data-odd')[1].split(' ')[1].replace('"', ''))
            data = {
                "o": res[0],
                "u": res[1],
            }
            return data
    except:
        return  {
            "o": '-',
            "u": '-',
        }


def getCoefBTS(idMatch):
    try:
        url = 'https://www.betexplorer.com/match-odds/%s/1/bts/' % idMatch
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            response = response.text.replace("\\", "")
            soup = BeautifulSoup(response, 'html.parser')
            table = soup.find('table', {'id':'sortable-1'})
            td = table.find_all('td', {'data-bid':'18'})
            res = []
            for t in td:
                res.append(str(t).replace('=', ' ').split('data-odd')[1].split(' ')[1].replace('"', ''))
            data = {
                "oz": res[0],
            }
            return data
    except:
        return  {
            "oz": '-',
        }


def getResult(link):
    try:
        idMatch = link.replace('/', ' ').split(' ')[-2]
        dataMatch = getDataMatch(link)
        mainCoef = getCoef1x2(idMatch)
        ouCoef = getCoefOU(idMatch)
        btsCoef = getCoefBTS(idMatch)
        if dataMatch and mainCoef:
            datafull = {**dataMatch, **mainCoef, **ouCoef, **btsCoef}
            datafull = json.dumps(datafull)
            with open(FILENAME, 'a') as output_file:
                output_file.write(str(datafull)+',\n')
            print('INFO: result OK, link', link)
        else:
            print('SKIP: dataMatch is bad, link', link)
    except Exception as e:
        print('SKIP: match is huinya', link, e )


def getDataFromFile():
    try:
        with open(FILENAME) as f:
            s = f.read()[:-1]
            s = str('[' + s[:-1] + ']') 
            data = json.loads(s)
        #os.remove(FILENAME)
        return data
    except Exception as e:
        print('ERROR: load data from file is failed', e)
        return None


if __name__ == "__main__":
    print('INFO: start script', str(dt.datetime.now()))
    start = dt.datetime.now()
    date_start = '2020-10-12' #yyyy-mm-dd
    date_end = '2021-02-01' #yyyy-mm-dd

    rangeDate = pd.date_range(date_start, date_end, freq='D')
    for date in rangeDate:
        d = date.date()
        url = 'https://www.betexplorer.com/results/soccer/?year=%s&month=%s&day=%s' % (d.year, d.month, d.day)
        print(url) 
        links = getAllLinks(url)
        if links != None and len(links) > 0:
            with Pool(8) as p:
                p.map(getResult, links)
        else:
            print("INFO: results of matches not found")
        time.sleep(5)
    
    df = pd.DataFrame(getDataFromFile())
    pathToFile = 'dataoutput_%s_%s.xlsx' % (date_start, date_end) 
    df.to_excel(pathToFile)    

    end = dt.datetime.now()
    total = end - start
    print('INFO: end script, total run time:',str(total))
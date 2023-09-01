import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import pandas as pd
import sqlite3
from bs4 import BeautifulSoup as BS
import math
import time
import sys

session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)


con = sqlite3.connect("db.sqlite")
cur = con.cursor()

if len(sys.argv) != 2:
	print('error: what year?!')
	sys.exit()

year = int(sys.argv[1])
print(year)
url = 'https://monitoring.miccedu.ru/?m=vpo&year='+str(year)
r = session.get(url)
r.encoding = r.apparent_encoding
page = BS(r.text, 'html.parser')

columns = []
uni_id_list = []
uni = []

start = time.time()

for state in page.select('p.MsoListParagraph a[href]'):  # through regions
    region_url = 'https://monitoring.miccedu.ru/' + state['href']
    r = session.get(region_url)
    r.encoding = r.apparent_encoding
    state_page = BS(r.content, features='lxml')
    regiontotal = len(state_page.select('.blockcontent tr td.inst a[href]'))
    regionname = state.get_text(separator = ' ')
    print('\033[1m{0}\033[0m ({1} университетов)'.format(regionname, regiontotal))
    regioni = 0
    for uni in state_page.select('.blockcontent tr td.inst a[href]'):  # through unis
        if (math.floor(100*regioni / regiontotal) % 10 == 0) and (math.floor(100*(regioni - 1) / regiontotal) % 10 != 0):
            print('{}% ({:.2f}s since start)'.format(math.floor(100*regioni / regiontotal), time.time() - start))
        regioni += 1;
        if uni['href'][:4] == 'http':
            continue
        uni_id = int(uni['href'][12:])
        uni_url = 'https://monitoring.miccedu.ru/iam/' + str(year) + '/_vpo/' + uni['href']
        r = session.get(uni_url)
        r.encoding = r.apparent_encoding
        uni_page = BS(r.content, features = 'lxml')
        name, address, ministry, website, owner = '', '', '', '', ''

        for indicator in uni_page.select('table#info tr'): # инфа
            fields = []
            for td in indicator.select('td'):
                fields.append(td.get_text(separator = ', '))
            if fields[0] == 'Наименование образовательной организации' and name == '':
                name = fields[1]
            elif fields[0] == 'Регион,, адрес':
                address = fields[1]
            elif fields[0] == 'Ведомственная принадлежность':
                ministry = fields[1]
            elif fields[0] == 'web-сайт':
                website = fields[1]
            elif fields[0] == 'Учредитель(и)':
                owner = fields[1]
        cur.execute('INSERT OR IGNORE INTO universities(uid, name, address, ministry, website, owner, fdid) VALUES(?,?,?,?,?,?, (SELECT fdid FROM federal_districts WHERE name = ?))', (uni_id, name, address, ministry, website, owner, regionname))
        con.commit()

        for indicator in uni_page.select('table#analis_dop tr'):  # доппоказатели
            fields = []
            td_num = len(indicator.find_all('td'))
            if td_num < 3:
                continue
            number, name, unit, value = '', '', '', 0
            for td in indicator.select('td'):
                fields.append(td.get_text(separator=' '))
            if fields[1] == 'Наименование показателя' or fields[1] == '2':
                continue
            if td_num == 4:
                cur.execute('INSERT OR IGNORE INTO indicators(number, name, unit) VALUES(?,?,?)',
                    (fields[0], fields[1], fields[2]))
                value = fields[3].replace(' ','').replace(',','.')
                if value == 'да':
                    value = 1
                elif value == 'нет':
                    value = 0
                cur.execute('''INSERT INTO data(uid, iid, year, value) VALUES(?,
                   (SELECT iid FROM indicators WHERE name = ?), ?, ?)''', (uni_id, fields[1], year, value))
            if td_num == 3:
                cur.execute('INSERT OR IGNORE INTO indicators(name, unit) VALUES(?,?)',
                    (fields[0], fields[1]))
                value = fields[2].replace(' ','').replace(',','.')
                cur.execute('''INSERT INTO data(uid, iid, year, value) VALUES(?,
                   (SELECT iid FROM indicators WHERE name = ?), ?, ?)''', (uni_id, fields[0], year, value))
        con.commit()

        for indicator in uni_page.select('table.napde tr'):  # мониторинг
            fields = []
            td_num = len(indicator.find_all('td'))
            if td_num == 4:  # skip headings and not full rows
                for td in indicator.select('td'):
                    fields.append(td.get_text(separator=' '))
                if fields[1] == 'Наименование показателя' or fields[1] == '2':
                    continue
                cur.execute('INSERT OR IGNORE INTO indicators(number, name, unit) VALUES(?,?,?)',
                    (fields[0], fields[1], fields[2]))
                value = fields[3].replace(' ','').replace(',','.')
                cur.execute('''INSERT INTO data(uid, iid, year, value) VALUES(?,
                   (SELECT iid FROM indicators WHERE name = ?), ?, ?)''', (uni_id, fields[1], year, value))
        con.commit()

        for indicator in uni_page.select('table#analis_reg tr'):  # УГНС
            fields = []
            td_num = len(indicator.find_all('td'))
            if td_num < 4:  # skip headings and not full rows
                continue;
            for td in indicator.select('td'):
                fields.append(td.get_text(separator=' '))
            if fields[0] == 'Реализуемые  УГН(С)' or fields[0] == 'Реализуемые УГН(С)':
                continue
            cur.execute('INSERT OR IGNORE INTO ugn(name) VALUES (?)', (fields[0],))
            value = fields[1].replace(' ','').replace(',','.')
            cur.execute('''INSERT INTO uni_ugn(ugnid, uid, year, people) VALUES((SELECT ugnid FROM ugn WHERE name = ?), ?, ?, ?)''', (fields[0], uni_id, year, value))
        con.commit()
    print('100% ({:.2f}s since start)'.format(time.time() - start))
con.close()

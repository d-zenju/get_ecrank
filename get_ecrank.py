# -*- coding: utf-8 -*-

import requests
import urllib2
import json
import sqlite3
import time
import datetime

import types

# リクエストURL(site name, categoryID, URL)
urls = [
    ['amazon', 'amazon0000', 'https://protected-beach-68433.herokuapp.com/index.php?site=amazon&categoryid=amazon0000&categorynum=2378086051&response=TopSellers&id=AKIAJP5XVIKHEQMB5XWA&sk=aGxwYy6%2FBpBRz42YY0GMWeZc6aIyVELZxWD7foQ%2B&ai=powerzport-22'],
    ['amazon', 'amazon0001', 'https://protected-beach-68433.herokuapp.com/index.php?site=amazon&categoryid=amazon0001&categorynum=2378233051&response=TopSellers&id=AKIAJP5XVIKHEQMB5XWA&sk=aGxwYy6%2FBpBRz42YY0GMWeZc6aIyVELZxWD7foQ%2B&ai=powerzport-22'],
    ['amazon', 'amazon0002', 'https://protected-beach-68433.herokuapp.com/index.php?site=amazon&categoryid=amazon0002&categorynum=2378232051&response=TopSellers&id=AKIAJP5XVIKHEQMB5XWA&sk=aGxwYy6%2FBpBRz42YY0GMWeZc6aIyVELZxWD7foQ%2B&ai=powerzport-22'],
    ['amazon', 'amazon0003', 'https://protected-beach-68433.herokuapp.com/index.php?site=amazon&categoryid=amazon0003&categorynum=2378230051&response=TopSellers&id=AKIAJP5XVIKHEQMB5XWA&sk=aGxwYy6%2FBpBRz42YY0GMWeZc6aIyVELZxWD7foQ%2B&ai=powerzport-22'],
    ['amazon', 'amazon0004', 'https://protected-beach-68433.herokuapp.com/index.php?site=amazon&categoryid=amazon0004&categorynum=2378229051&response=TopSellers&id=AKIAJP5XVIKHEQMB5XWA&sk=aGxwYy6%2FBpBRz42YY0GMWeZc6aIyVELZxWD7foQ%2B&ai=powerzport-22'],
    ['amazon', 'amazon0005', 'https://protected-beach-68433.herokuapp.com/index.php?site=amazon&categoryid=amazon0005&categorynum=2378225051&response=TopSellers&id=AKIAJP5XVIKHEQMB5XWA&sk=aGxwYy6%2FBpBRz42YY0GMWeZc6aIyVELZxWD7foQ%2B&ai=powerzport-22'],
    ['amazon', 'amazon0006', 'https://protected-beach-68433.herokuapp.com/index.php?site=amazon&categoryid=amazon0006&categorynum=2378224051&response=TopSellers&id=AKIAJP5XVIKHEQMB5XWA&sk=aGxwYy6%2FBpBRz42YY0GMWeZc6aIyVELZxWD7foQ%2B&ai=powerzport-22'],
    ['amazon', 'amazon0007', 'https://protected-beach-68433.herokuapp.com/index.php?site=amazon&categoryid=amazon0007&categorynum=2378231051&response=TopSellers&id=AKIAJP5XVIKHEQMB5XWA&sk=aGxwYy6%2FBpBRz42YY0GMWeZc6aIyVELZxWD7foQ%2B&ai=powerzport-22'],
    ['amazon', 'amazon0008', 'https://protected-beach-68433.herokuapp.com/index.php?site=amazon&categoryid=amazon0008&categorynum=2378226051&response=TopSellers&id=AKIAJP5XVIKHEQMB5XWA&sk=aGxwYy6%2FBpBRz42YY0GMWeZc6aIyVELZxWD7foQ%2B&ai=powerzport-22'],
    ['amazon', 'amazon0009', 'https://protected-beach-68433.herokuapp.com/index.php?site=amazon&categoryid=amazon0009&categorynum=2378228051&response=TopSellers&id=AKIAJP5XVIKHEQMB5XWA&sk=aGxwYy6%2FBpBRz42YY0GMWeZc6aIyVELZxWD7foQ%2B&ai=powerzport-22'],
    ['amazon', 'amazon0010', 'https://protected-beach-68433.herokuapp.com/index.php?site=amazon&categoryid=amazon0010&categorynum=2378425051&response=TopSellers&id=AKIAJP5XVIKHEQMB5XWA&sk=aGxwYy6%2FBpBRz42YY0GMWeZc6aIyVELZxWD7foQ%2B&ai=powerzport-22'],
    ['amazon', 'amazon0011', 'https://protected-beach-68433.herokuapp.com/index.php?site=amazon&categoryid=amazon0011&categorynum=268254011&response=TopSellers&id=AKIAJP5XVIKHEQMB5XWA&sk=aGxwYy6%2FBpBRz42YY0GMWeZc6aIyVELZxWD7foQ%2B&ai=powerzport-22'],
    ['amazon', 'amazon0012', 'https://protected-beach-68433.herokuapp.com/index.php?site=amazon&categoryid=amazon0012&categorynum=268258011&response=TopSellers&id=AKIAJP5XVIKHEQMB5XWA&sk=aGxwYy6%2FBpBRz42YY0GMWeZc6aIyVELZxWD7foQ%2B&ai=powerzport-22'],
    ['amazon', 'amazon0013', 'https://protected-beach-68433.herokuapp.com/index.php?site=amazon&categoryid=amazon0013&categorynum=268233011&response=TopSellers&id=AKIAJP5XVIKHEQMB5XWA&sk=aGxwYy6%2FBpBRz42YY0GMWeZc6aIyVELZxWD7foQ%2B&ai=powerzport-22'],
    ['amazon', 'amazon0014', 'https://protected-beach-68433.herokuapp.com/index.php?site=amazon&categoryid=amazon0014&categorynum=268273011&response=TopSellers&id=AKIAJP5XVIKHEQMB5XWA&sk=aGxwYy6%2FBpBRz42YY0GMWeZc6aIyVELZxWD7foQ%2B&ai=powerzport-22']
]

# スリープタイム
sleep_time = 2

# SQLite3 ディレクトリ名
dbpath = './'

# SQLite3 Create Table
create_table_sql = 'create table if not exists ecrank (site text, category_id text, unixtime integer, data text);'

# SQLite3 Insert data
insert_sql = 'insert into ecrank (site, category_id, unixtime, data) values (?, ?, ?, ?);'

def main():
    # SQLite3 DB名 ("PATH + YEAR + MONTH".sqlite3)
    today = datetime.datetime.today()
    dbname = dbpath + str(today.year) + '-' + str(today.month) + '.sqlite3'
    
    print 'Connect SQLite3 DB: ' + str(dbname)

    for url in urls:
        try:
            # get unixtime (now)
            funixtime = datetime.datetime.now()
            unixtime = int(time.mktime(funixtime.timetuple()))

            print str(unixtime) + ' "Request get data: (site, categoryID): [' + str(url[0]) + ', ' + str(url[1]) + ']"'

            # request URL
            jdatas = requests.get(url[2])
            jdata = jdatas.json()
            print jdatas

            # connect SQLite3
            sqlconnect = sqlite3.connect(dbname)
            cursor = sqlconnect.cursor()

            # create table
            cursor.execute(create_table_sql)

            # save json data
            values = (url[0], url[1], unixtime, str(jdata))
            cursor.execute(insert_sql, values)

            # commit SQLite3
            sqlconnect.commit()

            # Close SQLite3
            sqlconnect.close()

            # Access sleep
            time.sleep(sleep_time)

        except:
            print('Error. Try next category.')

if __name__ == '__main__':
    main()

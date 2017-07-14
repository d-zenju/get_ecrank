# -*- coding: utf-8 -*-

import sqlite3
import sqlite3
import time
import datetime
import requests
import base64

import types
import pprint


# リクエストURL(site name, categoryID, URL)
# yahoo : weekly/daily
# rakuten : realtimeは更新時間がまちまちなのでとりあえず何もしない

urls = [
    ['yahoo', 'yahoo0000', '3669', '布団・寝具' ,'weekly', 'https://shopping.yahooapis.jp/ShoppingWebService/V1/json/categoryRanking?appid=dj0zaiZpPXFMYmpXVVh3N2NmUyZzPWNvbnN1bWVyc2VjcmV0Jng9Nzg-&category_id=3669&period=weekly'],
    ['yahoo', 'yahoo0000', '3669', '布団・寝具' ,'daily', 'https://shopping.yahooapis.jp/ShoppingWebService/V1/json/categoryRanking?appid=dj0zaiZpPXFMYmpXVVh3N2NmUyZzPWNvbnN1bWVyc2VjcmV0Jng9Nzg-&category_id=3669&period=daily'],
    ['yahoo', 'yahoo0001', '27821', '枕・ピロー' ,'weekly', 'https://shopping.yahooapis.jp/ShoppingWebService/V1/json/categoryRanking?appid=dj0zaiZpPXFMYmpXVVh3N2NmUyZzPWNvbnN1bWVyc2VjcmV0Jng9Nzg-&category_id=27821&period=weekly'],
    ['yahoo', 'yahoo0001', '27821', '枕・ピロー' ,'daily', 'https://shopping.yahooapis.jp/ShoppingWebService/V1/json/categoryRanking?appid=dj0zaiZpPXFMYmpXVVh3N2NmUyZzPWNvbnN1bWVyc2VjcmV0Jng9Nzg-&category_id=27821&period=daily'],
    ['yahoo', 'yahoo0002', '27772', '布団セット' ,'weekly', 'https://shopping.yahooapis.jp/ShoppingWebService/V1/json/categoryRanking?appid=dj0zaiZpPXFMYmpXVVh3N2NmUyZzPWNvbnN1bWVyc2VjcmV0Jng9Nzg-&category_id=27772&period=weekly'],
    ['yahoo', 'yahoo0002', '27772', '布団セット' ,'daily', 'https://shopping.yahooapis.jp/ShoppingWebService/V1/json/categoryRanking?appid=dj0zaiZpPXFMYmpXVVh3N2NmUyZzPWNvbnN1bWVyc2VjcmV0Jng9Nzg-&category_id=27772&period=daily'],
    ['yahoo', 'yahoo0003', '48015', 'マットレス' ,'weekly', 'https://shopping.yahooapis.jp/ShoppingWebService/V1/json/categoryRanking?appid=dj0zaiZpPXFMYmpXVVh3N2NmUyZzPWNvbnN1bWVyc2VjcmV0Jng9Nzg-&category_id=48015&period=weekly'],
    ['yahoo', 'yahoo0003', '48015', 'マットレス' ,'daily', 'https://shopping.yahooapis.jp/ShoppingWebService/V1/json/categoryRanking?appid=dj0zaiZpPXFMYmpXVVh3N2NmUyZzPWNvbnN1bWVyc2VjcmV0Jng9Nzg-&category_id=48015&period=daily'],
    ['yahoo', 'yahoo0004', '48023', '敷きパッド' ,'weekly', 'https://shopping.yahooapis.jp/ShoppingWebService/V1/json/categoryRanking?appid=dj0zaiZpPXFMYmpXVVh3N2NmUyZzPWNvbnN1bWVyc2VjcmV0Jng9Nzg-&category_id=48023&period=weekly'],
    ['yahoo', 'yahoo0004', '48023', '敷きパッド' ,'daily', 'https://shopping.yahooapis.jp/ShoppingWebService/V1/json/categoryRanking?appid=dj0zaiZpPXFMYmpXVVh3N2NmUyZzPWNvbnN1bWVyc2VjcmV0Jng9Nzg-&category_id=48023&period=daily'],
    ['yahoo', 'yahoo0005', '27756', '敷き布団' ,'weekly', 'https://shopping.yahooapis.jp/ShoppingWebService/V1/json/categoryRanking?appid=dj0zaiZpPXFMYmpXVVh3N2NmUyZzPWNvbnN1bWVyc2VjcmV0Jng9Nzg-&category_id=27756&period=weekly'],
    ['yahoo', 'yahoo0005', '27756', '敷き布団' ,'daily', 'https://shopping.yahooapis.jp/ShoppingWebService/V1/json/categoryRanking?appid=dj0zaiZpPXFMYmpXVVh3N2NmUyZzPWNvbnN1bWVyc2VjcmV0Jng9Nzg-&category_id=27756&period=daily'],
    ['yahoo', 'yahoo0006', '27760', '掛け布団' ,'weekly', 'https://shopping.yahooapis.jp/ShoppingWebService/V1/json/categoryRanking?appid=dj0zaiZpPXFMYmpXVVh3N2NmUyZzPWNvbnN1bWVyc2VjcmV0Jng9Nzg-&category_id=27760&period=weekly'],
    ['yahoo', 'yahoo0006', '27760', '掛け布団' ,'daily', 'https://shopping.yahooapis.jp/ShoppingWebService/V1/json/categoryRanking?appid=dj0zaiZpPXFMYmpXVVh3N2NmUyZzPWNvbnN1bWVyc2VjcmV0Jng9Nzg-&category_id=27760&period=daily'],
    ['yahoo', 'yahoo0007', '3670', '布団カバー' ,'weekly', 'https://shopping.yahooapis.jp/ShoppingWebService/V1/json/categoryRanking?appid=dj0zaiZpPXFMYmpXVVh3N2NmUyZzPWNvbnN1bWVyc2VjcmV0Jng9Nzg-&category_id=3670&period=weekly'],
    ['yahoo', 'yahoo0007', '3670', '布団カバー' ,'daily', 'https://shopping.yahooapis.jp/ShoppingWebService/V1/json/categoryRanking?appid=dj0zaiZpPXFMYmpXVVh3N2NmUyZzPWNvbnN1bWVyc2VjcmV0Jng9Nzg-&category_id=3670&period=daily'],
    ['yahoo', 'yahoo0008', '27787', '毛布' ,'weekly', 'https://shopping.yahooapis.jp/ShoppingWebService/V1/json/categoryRanking?appid=dj0zaiZpPXFMYmpXVVh3N2NmUyZzPWNvbnN1bWVyc2VjcmV0Jng9Nzg-&category_id=27787&period=weekly'],
    ['yahoo', 'yahoo0008', '27787', '毛布' ,'daily', 'https://shopping.yahooapis.jp/ShoppingWebService/V1/json/categoryRanking?appid=dj0zaiZpPXFMYmpXVVh3N2NmUyZzPWNvbnN1bWVyc2VjcmV0Jng9Nzg-&category_id=27787&period=daily'],
    ['yahoo', 'yahoo0009', '3677', 'タオルケット' ,'weekly', 'https://shopping.yahooapis.jp/ShoppingWebService/V1/json/categoryRanking?appid=dj0zaiZpPXFMYmpXVVh3N2NmUyZzPWNvbnN1bWVyc2VjcmV0Jng9Nzg-&category_id=3677&period=weekly'],
    ['yahoo', 'yahoo0009', '3677', 'タオルケット' ,'daily', 'https://shopping.yahooapis.jp/ShoppingWebService/V1/json/categoryRanking?appid=dj0zaiZpPXFMYmpXVVh3N2NmUyZzPWNvbnN1bWVyc2VjcmV0Jng9Nzg-&category_id=3677&period=daily'],
    ['yahoo', 'yahoo0010', '48042', 'ドレープカーテン' ,'weekly', 'https://shopping.yahooapis.jp/ShoppingWebService/V1/json/categoryRanking?appid=dj0zaiZpPXFMYmpXVVh3N2NmUyZzPWNvbnN1bWVyc2VjcmV0Jng9Nzg-&category_id=48042&period=weekly'],
    ['yahoo', 'yahoo0010', '48042', 'ドレープカーテン' ,'daily', 'https://shopping.yahooapis.jp/ShoppingWebService/V1/json/categoryRanking?appid=dj0zaiZpPXFMYmpXVVh3N2NmUyZzPWNvbnN1bWVyc2VjcmV0Jng9Nzg-&category_id=48042&period=daily'],
    ['yahoo', 'yahoo0011', '48043', 'レースカーテン' ,'weekly', 'https://shopping.yahooapis.jp/ShoppingWebService/V1/json/categoryRanking?appid=dj0zaiZpPXFMYmpXVVh3N2NmUyZzPWNvbnN1bWVyc2VjcmV0Jng9Nzg-&category_id=48043&period=weekly'],
    ['yahoo', 'yahoo0011', '48043', 'レースカーテン' ,'daily', 'https://shopping.yahooapis.jp/ShoppingWebService/V1/json/categoryRanking?appid=dj0zaiZpPXFMYmpXVVh3N2NmUyZzPWNvbnN1bWVyc2VjcmV0Jng9Nzg-&category_id=48043&period=daily'],
    ['yahoo', 'yahoo0012', '48064', 'カーペット・ラグ' ,'weekly', 'https://shopping.yahooapis.jp/ShoppingWebService/V1/json/categoryRanking?appid=dj0zaiZpPXFMYmpXVVh3N2NmUyZzPWNvbnN1bWVyc2VjcmV0Jng9Nzg-&category_id=48064&period=weekly'],
    ['yahoo', 'yahoo0012', '48064', 'カーペット・ラグ' ,'daily', 'https://shopping.yahooapis.jp/ShoppingWebService/V1/json/categoryRanking?appid=dj0zaiZpPXFMYmpXVVh3N2NmUyZzPWNvbnN1bWVyc2VjcmV0Jng9Nzg-&category_id=48064&period=daily'],
    ['rakuten', 'rakuten0000', '215566', '寝具' ,'daily', 'https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20170628?applicationId=1042462765520193474&format=json&genreId=215566'],
    ['rakuten', 'rakuten0001', '564567', '枕・抱き枕' ,'daily', 'https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20170628?applicationId=1042462765520193474&format=json&genreId=564567'],
    ['rakuten', 'rakuten0002', '215613', '掛け敷き布団セット' ,'daily', 'https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20170628?applicationId=1042462765520193474&format=json&genreId=215613'],
    ['rakuten', 'rakuten0003', '508183', 'マットレス' ,'daily', 'https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20170628?applicationId=1042462765520193474&format=json&genreId=508183'],
    ['rakuten', 'rakuten0004', '551221', '敷きパッド・パッドシーツ' ,'daily', 'https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20170628?applicationId=1042462765520193474&format=json&genreId=551221'],
    ['rakuten', 'rakuten0005', '205555', '敷き布団' ,'daily', 'https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20170628?applicationId=1042462765520193474&format=json&genreId=205555'],
    ['rakuten', 'rakuten0006', '563689', '掛け布団' ,'daily', 'https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20170628?applicationId=1042462765520193474&format=json&genreId=563689'],
    ['rakuten', 'rakuten0007', '205604', '布団カバー' ,'daily', 'https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20170628?applicationId=1042462765520193474&format=json&genreId=205604'],
    ['rakuten', 'rakuten0008', '205611', '毛布' ,'daily', 'https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20170628?applicationId=1042462765520193474&format=json&genreId=205611'],
    ['rakuten', 'rakuten0009', '205613', 'タオルケット' ,'daily', 'https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20170628?applicationId=1042462765520193474&format=json&genreId=205613'],
    ['rakuten', 'rakuten0010', '300576', 'ドレープカーテン' ,'daily', 'https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20170628?applicationId=1042462765520193474&format=json&genreId=300576'],
    ['rakuten', 'rakuten0011', '300667', 'レースカーテン' ,'daily', 'https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20170628?applicationId=1042462765520193474&format=json&genreId=300667'],
    ['rakuten', 'rakuten0012', '551228', 'ラグ' ,'daily', 'https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20170628?applicationId=1042462765520193474&format=json&genreId=551228']
]


# Yahoo商品検索
yahoo_itemlookup_url = 'https://shopping.yahooapis.jp/ShoppingWebService/V1/json/itemLookup?appid=dj0zaiZpPXFMYmpXVVh3N2NmUyZzPWNvbnN1bWVyc2VjcmV0Jng9Nzg-&itemcode='

# スリープタイム
sleep_time = 2

# SQLite3 ディレクトリ名
dbpath = './db/'

# SQLite3 Create Table
create_table_sql_amazon = 'create table if not exists amazon (site text, category_id text, genre_id text, genre_name text, period text, unixtime text, rank text, item_id text, item_url text, item_name text, brand text, shop_name text, price text, sales_rank text, image_url text, image_data text);'
create_table_sql_rakuten = 'create table if not exists rakuten (site text, category_id text, genre_id text, genre_name text, period text, unixtime text, rank text, item_id text, item_url text, item_name text, shop_name text, shop_url text, price text, image_url text, image_data text);'
create_table_sql_yahoo = 'create table if not exists yahoo (site text, category_id text, genre_id text, genre_name text, period text, unixtime text, rank text, item_id text, item_url text, item_name text, shop_name text, shop_url text, price text, image_url text, image_data text);'

# SQLite3 Insert data
insert_sql_amazon = 'insert into amazon (site, category_id, genre_id, genre_name, period, unixtime, rank, item_id, item_url, item_name, brand, shop_name, price, sales_rank, image_url, image_data) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'
insert_sql_rakuten = 'insert into rakuten (site, category_id, genre_id, genre_name, period, unixtime, rank, item_id, item_url, item_name, shop_name, shop_url, price, image_url, image_data) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'
insert_sql_yahoo = 'insert into yahoo (site, category_id, genre_id, genre_name, period, unixtime, rank, item_id, item_url, item_name, shop_name, shop_url, price, image_url, image_data) values ('


def main():
    #while True:
        now_time = datetime.datetime.today()
        minute = now_time.minute
        second = now_time.second
        print 'GET ECRANK: ' + str(now_time)
        get_ecrank()
        #if minute == 0 and second == 0:
        #    print 'GET ECRANK: ' + str(now_time)
        #    get_ecrank()


def get_ecrank():
    # SQLite3 DB名 ("PATH + YEAR + MONTH".sqlite3)
    today = datetime.datetime.today()
    dbname = dbpath + str(today.year) + '-' + str(today.month) + '.sqlite3'
    
    print 'Connect SQLite3 DB: ' + str(dbname)

    for url in urls:
        try:
            # get unixtime (now)
            funixtime = datetime.datetime.now()
            unixtime = int(time.mktime(funixtime.timetuple()))

            print str(unixtime) + ' "Request get data: (site, categoryID): [' + str(url[0]) + ', ' + str(url[1]) + ', ' + str(url[3]) + ', ' + str(url[4]) + ']"'

            # request URL
            jsd = requests.get(url[5])
            if jsd.status_code == 200:
                print 'Get Data: Success'
            else:
                print 'Get Data: Error'

            # connect SQLite3
            sqlconnect = sqlite3.connect(dbname)
            cursor = sqlconnect.cursor()

            # create table
            if url[0] == 'amazon':
                cursor.execute(create_table_sql_amazon)
            if url[0] == 'rakuten':
                cursor.execute(create_table_sql_rakuten)
            if url[0] == 'yahoo':
                cursor.execute(create_table_sql_yahoo)

            # parse json datas
            jd = jsd.json()
            ## if 'yahoo' data
            if url[0] is 'yahoo':
                RankingData = jd['ResultSet']['0']['Result']
                for i in range(0, 20):
                    item_id = RankingData[str(i)]['Image']['Id']
                    item_url = RankingData[str(i)]['Url']
                    item_name = RankingData[str(i)]['Name']
                    shop_name = RankingData[str(i)]['Store']['Name']
                    shop_url = RankingData[str(i)]['Store']['Url']
                    image_url = RankingData[str(i)]['Image']['Medium']
                    rank = RankingData[str(i)]['_attributes']['rank']

                    # price
                    time.sleep(sleep_time)
                    purl = yahoo_itemlookup_url + item_id
                    pjsd = requests.get(purl)
                    pjd = pjsd.json()
                    price = pjd['ResultSet']['0']['Result']['0']['Price']['_value']
                    #image_data
                    img = requests.get(image_url)
                    if img.status_code == 200:
                        image_data = base64.urlsafe_b64encode(img.content)

                    # save data
                    insert_sql = 'insert into yahoo (site, category_id, genre_id, genre_name, period, unixtime, rank, item_id, item_url, item_name, shop_name, shop_url, price, image_url, image_data) values ("' + str(url[0]) + '", "' + str(url[1]) + '", "' + str(url[2]) + '", "' + str(url[3]) + '", "' + str(url[4]) + '", "' + str(unixtime) + '", "' + str(rank) + '", "' + item_id.encode('utf-8') + '", "' + item_url.encode('utf-8') + '", "' + item_name.encode('utf-8') + '", "' + shop_name.encode('utf-8') + '", "' + shop_url.encode('utf-8') + '", "' + price.encode('utf-8') + '", "' + image_url.encode('utf-8') + '", "' + str(image_data) + '");'
                    cursor.execute(insert_sql)

                    # commit SQLite3
                    sqlconnect.commit()
                    
            ## if 'rakuten' data
            if url[0] is 'rakuten':
                for i in range(0, 30):
                    item_id = jd['Items'][i]['Item']['itemCode']
                    item_url = jd['Items'][i]['Item']['itemUrl']
                    item_name = jd['Items'][i]['Item']['itemName']
                    shop_name = jd['Items'][i]['Item']['shopName']
                    shop_url = jd['Items'][i]['Item']['shopUrl']
                    price = jd['Items'][i]['Item']['itemPrice']
                    image_url = jd['Items'][i]['Item']['mediumImageUrls'][0]['imageUrl']
                    rank = jd['Items'][i]['Item']['rank']
                    
                    #image_data
                    img = requests.get(image_url)
                    if img.status_code == 200:
                        image_data = base64.urlsafe_b64encode(img.content)

                    # save data
                    insert_sql = 'insert into rakuten (site, category_id, genre_id, genre_name, period, unixtime, rank, item_id, item_url, item_name, shop_name, shop_url, price, image_url, image_data) values ("' + str(url[0]) + '", "' + str(url[1]) + '", "' + str(url[2]) + '", "' + str(url[3]) + '", "' + str(url[4]) + '", "' + str(unixtime) + '", "' + str(rank) + '", "' + item_id.encode('utf-8') + '", "' + item_url.encode('utf-8') + '", "' + item_name.encode('utf-8') + '", "' + shop_name.encode('utf-8') + '", "' + shop_url.encode('utf-8') + '", "' + price.encode('utf-8') + '", "' + image_url.encode('utf-8') + '", "' + str(image_data) + '");'
                    cursor.execute(insert_sql)
                    
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
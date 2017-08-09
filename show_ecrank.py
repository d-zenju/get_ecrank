# -*- coding: utf-8 -*-
from bottle import route, get, post, request, run, template
import sqlite3
import xlsxwriter
import glob
from datetime import *
import time
import json
from ast import literal_eval
import os
import types
import string

# DBディレクトリ名
amazon_db_path = './db/'
yahoo_db_path = './rakuten_yahoo/db/'
rakuten_db_path = './rakuten_yahoo/db/'

# Excelファイルパス
excel_path = './result.xlsx'

# 取得日時フォーマット
date_format = '%Y/%m/%d %H:00'


# カテゴリリスト
category_name = {"amazon0000":"寝具",
                "amazon0001":"枕・抱き枕",
                "amazon0002":"布団セット",
                "amaozn0003":"マットレス",
                "amazon0004":"ベットパッド・敷きパッド",
                "amazon0005":"敷きふとん",
                "amazon0006":"掛けふとん",
                "amazon0007":"寝具カバー・シーツ",
                "amaozn0008":"毛布",
                "amazon0009":"タオルケット・ガーゼケット",
                "amazon0010":"キッズ・ジュニア用寝具",
                "amazon0011":"カーテン",
                "amazon0012":"レースカーテン",
                "amazon0013":"ラグ・カーペット",
                "amazon0014":"クッション・クッションカバー"}


# Webアプリケーション(get: category_id, unixtime)
@get('/show/:site')
def select(site):
    # サイト名判定(title用)
    if (site == 'amazon'):
        site_name = 'Amazon.co.jp'
    elif (site == 'yahoo'):
        site_name = 'Yahoo!ショッピング'
    elif (site == 'rakuten'):
        site_name = '楽天市場'
    else:
        site_name = ''
    
    # 特定のサイトの取得日時とDB名を取得する
    categories, dates = list_dates(site)
   
    return template('select', site=site, site_name=site_name, categories=sorted(categories), dates=dates)


# Webアプリケーション(post: category_id, unixtime)
@post('/show/:site')
def show(site):
    # @getより取得
    site_name = request.forms.get('site_name')
    category_id = request.forms.get('selectName1')
    unixtime = request.forms.getall('selectName2')


    dates = []
    for utime in unixtime:
        dates.append(datetime.fromtimestamp(int(utime)).strftime(date_format))

    # サイト名判定(title用)
    if (site_name == 'amazon'):
        siteName = 'Amazon.co.jp'
    elif (site_name == 'yahoo'):
        siteName = 'Yahoo!ショッピング'
    elif (site_name == 'rakuten'):
        siteName = '楽天市場'
    else:
        siteName = ''

    datas = []

    for utime in unixtime:
        # DBファイル名
        if (site_name == 'amazon'):
            db_name = amazon_db_path + sqlite_filename(int(utime))
        elif (site_name == 'yahoo'):
            db_name = yahoo_db_path + sqlite_filename(int(utime))
        elif (site_name == 'rakuten'):
            db_name = rakuten_db_path + sqlite_filename(int(utime))
        print db_name

        # DB接続
        connect = sqlite3.connect(db_name)
        cursor = connect.cursor()

        if (site_name == 'amazon'):
            sql = 'select distinct data from ecrank where site="' + str(site_name) + '" and category_id="' + str(category_id) + '" and unixtime="' + str(utime) + '"'
        else:
            sql = 'select distinct * from ' + str(site_name) + ' where category_id="' + str(category_id) + '" and unixtime="' + str(utime) + '"'
    
        rows = cursor.execute(sql)

        if (site_name == 'amazon'):
            for row in rows:
                d = row[0]

            try:
                jd = json.loads(d)
            except:
                jd = literal_eval(d)
        
            datas.append(jd)
        
            # DB接続解除
            connect.close()

            return template('show', siteName=siteName, jdata=datas, dates=dates, category_name=category_name)

        else:
            return template('show_ry', siteName=siteName, rows=rows, dates=dates)

    #for data in datas:
    #    jdata = json.loads(data)
    #    print json.dumps(jdata, sort_keys = True, indent = 4)


def main():
    site = 'yahoo'
    site_name = 'yahoo'
    category_id = 'yahoo0012'
    unixtime = [1502262918]

    for utime in unixtime:
        # DBファイル名
        if (site == 'amazon'):
            db_name = amazon_db_path + sqlite_filename(int(utime))
        elif (site == 'yahoo'):
            db_name = yahoo_db_path + sqlite_filename(int(utime))
        elif (site == 'rakuten'):
            db_name = rakuten_db_path + sqlite_filename(int(utime))
        print db_name

    # DB接続
    connect = sqlite3.connect(db_name)
    cursor = connect.cursor()

    if (site == 'amazon'):
        sql = 'select distinct data from ecrank where site="' + str(site_name) + '" and category_id="' + str(category_id) + '" and unixtime="' + str(utime) + '"'
    else:
        sql = 'select distinct * from ' + str(site) + ' where category_id="' + str(category_id) + '" and unixtime="' + str(utime) + '" order by rank asc'
    
    print sql
    rows = cursor.execute(sql)

    for row in rows:
        print row


# SQLite3のファイル名
def sqlite_filename(unixtime):
    date = datetime.fromtimestamp(unixtime)
    return str(date.year) + '-' + str(date.month) + '.sqlite3'


# ディレクトリ内のDBからunixtime, date, pathの一覧をlist型で取得する
def list_dates(site):
    categories = []
    db_unixtimes = []
    date_dbname_list = []
    date_dict = {}
    uniq_data_list = []

    # ディレクトリ内のsqlite3を探査
    if (site == 'amazon'):
        dpath = amazon_db_path + "*.sqlite3"
    elif (site == 'yahoo'):
        dpath = yahoo_db_path + "*.sqlite3"
    elif (site == 'rakuten'):
        dpath = rakuten_db_path + "*.sqlite3"
    print dpath
    db_list = glob.glob(dpath)

    for db_name in db_list:
        # DB接続
        connect = sqlite3.connect(db_name)
        cursor = connect.cursor()

        # category_id, unixtime一覧取得
        if (site == 'amazon'):
            sql = 'select distinct category_id, unixtime from ecrank where site="' + str(site) + '" order by category_id asc, unixtime asc'
        else:
            sql = 'select distinct category_id, unixtime from ' + str(site) + ' order by category_id asc, unixtime asc'
        
        print sql
        rows = cursor.execute(sql)

        dates_list = []
        for row in rows:
            categories.append(row[0])
            read_date = datetime.fromtimestamp(int(row[1])).strftime(date_format)
            dates_list.append([row[0], read_date, row[1]])

        # category_id一覧(重複なし)
        categories_id = list(set(categories))

        for ci in categories_id:
            dates_dict = {}
            for dl in dates_list:
                if dl[0] == ci:
                    dates_dict[dl[1]] = dl[2]
            dd_key = sorted(list(dates_dict))
            dd_value = sorted(dates_dict.values())

            for i, dd in enumerate(dd_key):
                uniq_data_list.append([ci, dd_key[i], dd_value[i]])
        
    for d in uniq_data_list:
        print d

    return categories_id, uniq_data_list


# unixtimeの一覧からdatetime(重複あり)のlist型に変換
def uniq_datetime(unixtimes, format):
    dates = []
    for unixtime in unixtimes:
        dates.append(datetime.fromtimestamp(unixtime).strftime(format))
    return dates


# datetimeの一覧からunixtime(重複あり)のlist型に変換
def uniq_unixtime(dates, format):
    unixtimes = []
    for date in dates:
        unixtimes.append(int(time.mktime(datetime.strptime(date, format).timetuple())))
    return unixtimes


run(host='localhost', port=8080, debug=True, reloader=False)

if __name__ == '__main__':
    main()
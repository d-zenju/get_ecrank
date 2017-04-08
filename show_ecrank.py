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

# DBディレクトリ名
db_path = './*.sqlite3'

# Excelファイルパス
excel_path = './result.xlsx'

# 取得日時フォーマット
date_format = '%Y/%m/%d %H:00'


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
        db_name = sqlite_filename(int(utime))

        # DB接続
        connect = sqlite3.connect(db_name)
        cursor = connect.cursor()

        sql = 'select distinct data from ecrank where site="' + str(site_name) + '" and category_id="' + str(category_id) + '" and unixtime="' + str(utime) + '"'
        rows = cursor.execute(sql)

        for row in rows:
            d = row[0]
        #jd = json.loads(d)
        jd = literal_eval(d)
        datas.append(jd)
        
        # DB接続解除
        connect.close()

    return template('show', siteName=siteName, jdata=datas, dates=dates)

    #for data in datas:
    #    jdata = json.loads(data)
    #    print json.dumps(jdata, sort_keys = True, indent = 4)


def main():
    site = 'amazon'
    site_name = 'amazon'
    category_id = 'amazon0000'
    unixtime = [1491138105]

    # 特定のサイトの取得日時とDB名を取得する
    categories, dates = list_dates(site)

    datas = []

    for utime in unixtime:
        # DBファイル名
        db_name = sqlite_filename(int(utime))

        # DB接続
        connect = sqlite3.connect(db_name)
        cursor = connect.cursor()

        sql = 'select distinct data from ecrank where site="' + str(site_name) + '" and category_id="' + str(category_id) + '" and unixtime="' + str(utime) + '"'
        rows = cursor.execute(sql)

        for i, row in enumerate(rows):
            data = row[0]
            if i == 0:
                print json.loads(data)
        
        # DB接続解除
        connect.close()
    
    for data in datas:
        for d in data:
            print type(d)


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

    # ディレクトリ内のsqlite3を探査
    db_list = glob.glob(db_path)

    for db_name in db_list:
        # DB接続
        connect = sqlite3.connect(db_name)
        cursor = connect.cursor()

        # category_id, unixtime一覧取得
        sql = 'select distinct category_id, unixtime from ecrank where site="' + str(site) + '" order by category_id asc, unixtime asc'
        rows = cursor.execute(sql)

        dates_list = []
        for row in rows:
            categories.append(row[0])
            read_date = datetime.fromtimestamp(int(row[1])).strftime(date_format)
            dates_list.append([row[0], read_date, row[1]])

        # category_id一覧(重複なし)
        categories_id = list(set(categories))

        uniq_data_list = []
        for ci in categories_id:
            dates_dict = {}
            for dl in dates_list:
                if dl[0] == ci:
                    dates_dict[dl[1]] = dl[2]
            dd_key = sorted(list(dates_dict))
            dd_value = sorted(dates_dict.values())

            for i, dd in enumerate(dd_key):
                uniq_data_list.append([ci, dd_key[i], dd_value[i]])

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
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
import base64
import io
import urllib2

# DBディレクトリ名
amazon_db_path = './db/'
yahoo_db_path = './rakuten_yahoo/db/'
rakuten_db_path = './rakuten_yahoo/db/'

# Excelファイルパス
xlsx_path = './xlsx_files/'
xlsx_path_ry = './rakuten_yahoo/xlsx_files/'

# 取得日時フォーマット
#date_format = '%Y/%m/%d %H:00'
date_format = '%Y/%m/%d'


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
                "amazon0014":"クッション・クッションカバー",
                "amazon0015":"ベッド",
                "amazon0016":"ソファ・カウチ",
                "amazon0017":"ソファベッド",
                "amazon0018":"ラグ・カーペット・マット"}


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
            sql = 'select distinct * from ' + str(site_name) + ' where category_id="' + str(category_id) + '" and unixtime="' + str(utime) + '" and period="daily"'
    
        rows = cursor.execute(sql)

        if (site_name == 'amazon'):
            for row in rows:
                d = row[0]

            try:
                jd = json.loads(d)
            except:
                jd = literal_eval(d)
        
            datas.append(jd)
        
        else:
            d = []
            for row in rows:
                d.append(row)
            datas.append(d)

        # DB接続解除
        connect.close()

    if (site_name == 'amazon'):
        make_xlsx_amazon(datas, dates)
        return template('show', siteName=siteName, jdata=datas, dates=dates, category_name=category_name)
    else:
        make_xlsx_rakuten_yahoo(site_name, datas, dates)
        return template('show_ry', siteName=siteName, rows=datas, dates=dates)

    #for data in datas:
    #    jdata = json.loads(data)
    #    print json.dumps(jdata, sort_keys = True, indent = 4)
    print 'show'

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


# Excel(xlsx)ファイル出力
def make_xlsx_amazon(jdatas, dates):
    filename = xlsx_path + 'Amazon_' + category_name[jdatas[0][0]['category_id']] + '.xlsx'

    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()

    # column size
    ## rank
    worksheet.set_column(0, 0, 5)
    ## columns
    for i in range(100):
        worksheet.set_column(i*2+1, i*2+1, 14)
        worksheet.set_column(i*2+2, i*2+2, 25)
    ## rows
    for i in range(10):
        worksheet.set_row(3+i*5, 54)
        worksheet.set_row(4+i*5, 20)
        worksheet.set_row(5+i*5, 20)
        worksheet.set_row(6+i*5, 20)
        worksheet.set_row(7+i*5, 20)
    
    # format
    ## item title
    item_title_format = workbook.add_format()
    item_title_format.set_text_wrap()
    item_title_format.set_align('vcenter')
    item_title_format.set_font_color('blue')
    item_title_format.set_right(1)
    item_title_format.set_top(1)
    ## rank
    rank_format = workbook.add_format()
    rank_format.set_align('center')
    rank_format.set_align('vcenter')
    rank_format.set_bold()
    rank_format.set_border(1)
    ## date
    date_format = workbook.add_format()
    date_format.set_align('center')
    date_format.set_align('vcenter')
    date_format.set_bold()
    date_format.set_border(1)
    ## price
    price_format = workbook.add_format()
    price_format.set_font_color('red')
    price_format.set_num_format(u'¥#,##0')
    price_format.set_align('center')
    price_format.set_align('vcenter')
    price_format.set_right(1)
    price_format.set_bottom(1)
    ## default
    default_format = workbook.add_format()
    default_format.set_align('center')
    default_format.set_align('vcenter')
    default_format.set_right(1)
    ## category title
    category_title_format = workbook.add_format()
    category_title_format.set_font_size(16)
    ## rank 10 image(bottom)
    bottom_format = workbook.add_format()
    bottom_format.set_bottom(1)
    bottom_format.set_align('center')
    bottom_format.set_align('vcenter')
    ## image
    image_format = workbook.add_format()
    image_format.set_align('center')
    image_format.set_align('vcenter')

    # category title
    category_title = 'Amazon.co.jp 週別売上カテゴリランキング （' + category_name[jdatas[0][0]['category_id']] + '）'
    worksheet.write(0, 0, category_title.decode('utf-8'), category_title_format)

    # date
    for col, date in enumerate(dates):
        worksheet.merge_range(2, 1+2*col, 2, 2+2*col, date, date_format)
    
    # item
    for row in range(10):
        for col in range(len(dates)):
            worksheet.merge_range(3+5*row, 1+2*col, 3+5*row, 2+2*col, jdatas[col][row]['title'], item_title_format)
            worksheet.write(4+5*row, 2+2*col, jdatas[col][row]['asin'], default_format)
            worksheet.write(5+5*row, 2+2*col, jdatas[col][row]['shop'], default_format)
            worksheet.write(6+5*row, 2+2*col, 'SR: ' + jdatas[col][row]['sales_rank'], default_format)
            worksheet.write(7+5*row, 2+2*col, int(jdatas[col][row]['price']), price_format)
            if row is 9:
                worksheet.merge_range(4+5*row, 1+2*col, 7+5*row, 1+2*col, '', bottom_format)
            else:
                worksheet.merge_range(4+5*row, 1+2*col, 7+5*row, 1+2*col, '')
            img = io.BytesIO(base64.b64decode(jdatas[col][row]['img_data']))
            worksheet.insert_image(4+5*row, 1+2*col, jdatas[col][row]['img_url'], {'image_data': img, 'x_scale': 0.6, 'y_scale':0.6, 'x_offset': 1, 'y_offset': 1})

    # rank
    worksheet.write(2, 0, 'Rank', rank_format)
    for rank in range(10):
        worksheet.merge_range(3+5*rank, 0, 7+5*rank, 0, rank+1, rank_format)

    workbook.close()


# Excel(xlsx)ファイル出力(Rakuten, Yahoo!)
def make_xlsx_rakuten_yahoo(site_name, datas, dates):
    if (site_name == 'rakuten'):
        filename = xlsx_path_ry + u'楽天_' + datas[0][0][3] + u'.xlsx'
    else:        
        filename = xlsx_path_ry + u'Yahoo_' + datas[0][0][3] + u'.xlsx'
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()

    # column size
    ## rank
    worksheet.set_column(0, 0, 5)
    ## columns
    for i in range(100):
        worksheet.set_column(i*2+1, i*2+1, 14)
        worksheet.set_column(i*2+2, i*2+2, 25)
    ## rows
    for i in range(10):
        worksheet.set_row(3+i*4, 54)
        worksheet.set_row(4+i*4, 30)
        worksheet.set_row(5+i*4, 30)
        worksheet.set_row(6+i*4, 30)
    
    # format
    ## item title
    item_title_format = workbook.add_format()
    item_title_format.set_text_wrap()
    item_title_format.set_align('vcenter')
    item_title_format.set_font_color('blue')
    item_title_format.set_right(1)
    item_title_format.set_top(1)
    ## rank
    rank_format = workbook.add_format()
    rank_format.set_align('center')
    rank_format.set_align('vcenter')
    rank_format.set_bold()
    rank_format.set_border(1)
    ## date
    date_format = workbook.add_format()
    date_format.set_align('center')
    date_format.set_align('vcenter')
    date_format.set_bold()
    date_format.set_border(1)
    ## price
    price_format = workbook.add_format()
    price_format.set_font_color('red')
    price_format.set_num_format(u'¥#,##0')
    price_format.set_align('center')
    price_format.set_align('vcenter')
    price_format.set_right(1)
    price_format.set_bottom(1)
    ## default
    default_format = workbook.add_format()
    default_format.set_align('center')
    default_format.set_align('vcenter')
    default_format.set_right(1)
    ## category title
    category_title_format = workbook.add_format()
    category_title_format.set_font_size(16)
    ## rank 10 image(bottom)
    bottom_format = workbook.add_format()
    bottom_format.set_bottom(1)
    bottom_format.set_align('center')
    bottom_format.set_align('vcenter')
    ## image
    image_format = workbook.add_format()
    image_format.set_align('center')
    image_format.set_align('vcenter')

    # category title
    if(site_name == 'rakuten'):
        category_title = u'楽天市場 週別売上カテゴリランキング （' + datas[0][0][3] + u'）'
    else:
        category_title = u'Yahoo!ショッピング 週別売上カテゴリランキング （' + datas[0][0][3] + u'）'

    worksheet.write(0, 0, category_title, category_title_format)

    # date
    for col, date in enumerate(dates):
        worksheet.merge_range(2, 1+2*col, 2, 2+2*col, date, date_format)
    
    # item
    for row in range(10):
        for col in range(len(dates)):
            worksheet.merge_range(3+4*row, 1+2*col, 3+4*row, 2+2*col, datas[col][row][9], item_title_format)
            worksheet.write(4+4*row, 2+2*col, datas[col][row][7], default_format)
            worksheet.write(5+4*row, 2+2*col, datas[col][row][10], default_format)
            worksheet.write(6+4*row, 2+2*col, int(datas[col][row][12]), price_format)
            if row is 9:
                worksheet.merge_range(4+4*row, 1+2*col, 6+4*row, 1+2*col, '', bottom_format)
            else:
                worksheet.merge_range(4+4*row, 1+2*col, 6+4*row, 1+2*col, '')
            img = io.BytesIO(urllib2.urlopen(datas[col][row][13]).read())
            worksheet.insert_image(4+4*row, 1+2*col, datas[col][row][13], {'image_data': img, 'x_scale': 0.6, 'y_scale':0.6, 'x_offset': 1, 'y_offset': 1})
            
    # rank
    worksheet.write(2, 0, 'Rank', rank_format)
    for rank in range(10):
        worksheet.merge_range(3+4*rank, 0, 6+4*rank, 0, rank+1, rank_format)

    workbook.close()


run(host='localhost', port=8080, debug=True, reloader=False)


if __name__ == '__main__':
    main()
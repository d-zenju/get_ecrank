# -*- coding: utf-8 -*-

from bottle import route, run, get, post, template, error
import sqlite3
import glob
from datetime import *



# DBディレクトリ名
db_path = './db/'

# 日時フォーマット
date_format = '%Y/%m/%d %H:00'


@get('/rakuten')
def rakuten_select():
    categories, dates = list_dates('rakuten')
    print categories
    return template('rakuten_select', categories=sorted(categories), dates=dates)

@post('/rakuten')
def rakuten_show():
    return "show"


def main():
    categories, dates = list_dates('rakuten')
    print categories


# ディレクトリ内のDBからunixtime, date, pathの一覧をlist型で取得する
def list_dates(site):
    categories = []
    db_unixtimes = []
    date_dbname_list = []
    date_dict = {}
    uniq_data_list = []

    # ディレクトリ内のsqlite3を探査
    dpath = db_path + "*.sqlite3"
    print dpath
    db_list = glob.glob(dpath)

    for db_name in db_list:
        # DB接続
        connect = sqlite3.connect(db_name)
        cursor = connect.cursor()

        print "connect SQLITE3"

        # category_id, unixtime一覧取得
        sql = 'select distinct category_id, unixtime from ' + str(site) + ' order by category_id asc, unixtime asc'
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


run(localhost='localhost', port='8080', debug=True)

if __name__ == '__main__':
    main()
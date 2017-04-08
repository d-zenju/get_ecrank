# -*- coding: utf-8 -*-

import glob
import sqlite3
from datetime import *
import time

# DBディレクトリ名
db_path = './*.sqlite3'

# 取得日時フォーマット
date_format = '%Y/%m/%d %H:00'


def main():
    # ディレクトリ内のsqlite3を探査
    db_list = glob.glob(db_path)

    for db_name in db_list:
        # DB接続
        connect = sqlite3.connect(db_name)
        cursor = connect.cursor()

        # category_id, unixtime一覧取得
        sql = 'select * from ecrank order by site asc, category_id asc, unixtime asc'
        rows = cursor.execute(sql)

        for row in rows:
            date = unixtime_to_datetime(row[2], date_format)
            unixtime = datetime_to_unixtime(date, date_format)
            print row[0], row[1], row[2], date, unixtime


# unixtimeからdatetimeに変換
def unixtime_to_datetime(unixtime, format):
    return datetime.fromtimestamp(unixtime).strftime(format)

# datetimeからunixtimeに変換
def datetime_to_unixtime(date, format):
    return int(time.mktime(datetime.strptime(date, format).timetuple()))


if __name__ == '__main__':
    main()
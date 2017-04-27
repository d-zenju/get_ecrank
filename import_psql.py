# -*- coding: utf-8 -*-

import subprocess
import sqlite3
import csv
import time
from datetime import *

csv.field_size_limit(1000000000)

DATABASE_URL = 'postgres://eozupspbuhupic:f54530f991dd9ad6e15e9ce77f24b1170d7f29bffcb5da6378303f07f3878e49@ec2-23-23-93-255.compute-1.amazonaws.com:5432/d6r5f2uoeq439m'
DATABASE_TABLE = 'ecrank'
CSV_FILENAME = 'psql.csv'

# DBディレクトリ名
db_path = './db/'

# 取得日時フォーマット
date_format = '%Y/%m/%d %H:00'

# SQLite3 Create Table
create_table_sql = 'create table if not exists ecrank (site text, category_id text, unixtime integer, data text);'

# SQLite3 Insert data
insert_sql = 'insert into ecrank (site, category_id, unixtime, data) values (?, ?, ?, ?);'


def main():
    psql_download()
    csv2sqlite()
    remove_csv()


# heroku上Postgresをダウンロード -> '|'区切りCSV
def psql_download():
    cmd = 'psql ' + str(DATABASE_URL) + ' ' + str(DATABASE_TABLE) + ' -c "select * from ' + str(DATABASE_TABLE) + '" -A -t > ' + str(CSV_FILENAME)
    print 'Download psql > ' + str(CSV_FILENAME)
    subprocess.call( cmd , shell=True )
    print 'Done'


# '|'区切りCSVからSQLite3に変換
def csv2sqlite():
    print 'Import csv to sqlite3'
    reader = csv.reader(open(CSV_FILENAME), delimiter='|')

    for i, row in enumerate(reader):
        site = row[0]
        category_id = row[1]
        unixtime = row[2]
        data = row[3]
        values = (site, category_id, unixtime, data)

        # SQLite3ファイル名
        db_filename = sqlite_filename(int(unixtime))

        print str(i) + ': import datas --> ' + str(db_filename)
        
        # connect SQLite3
        sqlconnect = sqlite3.connect(db_filename)
        sqlconnect.text_factory = str  
        cursor = sqlconnect.cursor()

        # create table
        cursor.execute(create_table_sql)

        # save json data
        cursor.execute(insert_sql, values)

        # commit SQLite3
        sqlconnect.commit()

        # Close SQLite3
        sqlconnect.close()


# SQLite3のファイル名
def sqlite_filename(unixtime):
    date = datetime.fromtimestamp(unixtime)
    return db_path + str(date.year) + '-' + str(date.month) + '.sqlite3'


# CSVファイル削除
def remove_csv():
    print 'Remove ' + str(CSV_FILENAME)
    cmd = 'rm ' + str(CSV_FILENAME)
    subprocess.call( cmd , shell=True )
    print 'Done'


if __name__ == '__main__':
    main()

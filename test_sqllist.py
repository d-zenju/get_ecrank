# -*- coding: utf-8 -*-

import sqlite3
import json
import types
from ast import literal_eval
import string


connect = sqlite3.connect('2017-4.sqlite3')
cursor = connect.cursor()

sql = 'select data from ecrank where site="amazon" and category_id="amazon0000" and unixtime="1491660497"'
rows = cursor.execute(sql)

for row in rows:
    data = row[0]

jd = literal_eval(data)
print jd[0]['img_data'].replace('\/', '/')

#jdata = json.loads(data)

#print jdata[0]['shop']

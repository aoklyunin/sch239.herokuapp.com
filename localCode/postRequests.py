# coding=utf-8
import urllib

import urllib.request
import urllib.parse
import datetime

now_date = datetime.date.today()  # Текущая дата (без времени)

delta = datetime.timedelta(days=30)  # дельта в 2 дня
now_date = now_date - delta  # или какое число было 2 дня назад

data = {"begin_date": now_date,
        "end_date": datetime.date.today()}
enc_data = urllib.parse.urlencode(data)

print(enc_data.encode('utf-8'))
# POST запрос
f = urllib.request.urlopen("http://0.0.0.0:5000/getTasks/", enc_data.encode('utf-8'))
print(f.read())
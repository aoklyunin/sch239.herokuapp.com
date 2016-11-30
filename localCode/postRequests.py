# coding=utf-8
# модуль для теста post-запроса, возвращающего список заданий в заданном диапазоне
import urllib.parse
import datetime


now_date = datetime.date.today()  # Текущая дата (без времени)
delta = datetime.timedelta(days=30)  # дельта в 30 дней
now_date = now_date - delta  # или какое число было 30 дней назад
# данные запроса
data = {"begin_date": now_date,
        "end_date": datetime.date.today()}
enc_data = urllib.parse.urlencode(data)
# выводим данные
print(enc_data.encode('utf-8'))
# POST запрос
f = urllib.request.urlopen("http://0.0.0.0:5000/getTasks/", enc_data.encode('utf-8'))
# выводим ответ на запрос
print(f.read())
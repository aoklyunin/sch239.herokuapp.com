# -*- coding: utf-8 -*-
from localCode.customOperation import transliterate, password_generator

from sworks.models import Student,User

arr = [ [u'Абдурахманов Рауль',1],
        [u'Бей Святослав',1],
        [u'Берхман Евгений',1],
        [u'Ведь Олеся',1],
        [u'Винникова Анна',1],
        [u'Вьюгинов Андрей',1],
        [u'Грачев Иван',1],
        [u'Грек Полина',1],
        [u'Димитров Благой',1],
        [u'Еремеев Иван',1],
        [u'Звонов Даниил',1],
        [u'Златковский Марк',1],
        [u'Зорин Андрей',1],
        [u'Иванова Марианна',1],
        [u'Игнатьев Артур',2],
        [u'Козар Илья',2],
        [u'Котова Олеся',2],
        [u'Лабес Алена',2],
        [u'Мартыненко Анастасия',2],
        [u'Никитин Михаил',2],
        [u'Нургалиев Артём',2],
        [u'Нургалиев Тимур',2],
        [u'Попелышко Аким',2],
        [u'Смирнов Даниил',2],
        [u'Смирнов Михаил',2],
        [u'Ширшин Даниил',2]]


#users = User.objects.all()
#fo#r us in users:
    #print(us.username)
for a in arr:
    #print (a)
    s = a[0].split(" ")
#    print(a[1])
    name = s[1]
    second_name = s[0]
    group = a[1]
    if not User.objects.filter(first_name = name,last_name=second_name).exists():
        username = transliterate(name[:1])+transliterate(second_name).lower()
        password = password_generator(8)
        print (transliterate(name)+u" "+transliterate(second_name) + u" "+username+u" "+password)
        #print(name," ",second_name)
# -*- coding: utf-8 -*-
from sworks.models import Student,User
from localCode.customOperation import transliterate, password_generator

arr = [
[u'Благой Димитров', u'dimitrovblagoi@gmail.com',1],
[u'Святослав Бей', u'bey.sviatoslav@yandex.ru',1],
[u'Артур Игнатьев', u'artur23924@bk.ru',2],
[u'Смирнов Даниил', u'sdaniil@gmail.com',2]]

for a in arr:
    #print (a)
    s = a[0].split(" ")
#    print(a[1])
    name = s[1]
    second_name = s[0]
    group = a[1]
    username = transliterate(name[:1])+transliterate(second_name).lower()
    password = password_generator(8)
    print (transliterate(name)+u" "+transliterate(second_name) + u" "+username+u" "+password)
    user =  User.objects.create_user(username=username, email=a[1], password=password)
    user.first_name = name
    user.last_name = second_name
    user.save()
    student = Student.objects.create(user=user,st_klass='10-3',st_group=a[2])
    student.save()
        #print(name," ",second_name)
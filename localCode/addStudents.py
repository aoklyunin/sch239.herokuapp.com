# -*- coding: utf-8 -*-
# модуль для создания пользователей из списка
from localCode.customOperation import transliterate, password_generator
from sworks.models import Student, User

# массив записей
arr = [
    [u'Благой Димитров', u'dimitrovblagoi@gmail.com', 1],
    [u'Святослав Бей', u'bey.sviatoslav@yandex.ru', 1],
    [u'Артур Игнатьев', u'artur23924@bk.ru', 2],
    [u'Смирнов Даниил', u'sdaniil@gmail.com', 2]]

# проходим по массиву
for a in arr:
    # получаем имя и фамилию
    s = a[0].split(" ")
    name = s[1]
    second_name = s[0]
    # получаем номер группы
    group = a[1]
    # генерируем логин на основе имени и фамилии
    username = transliterate(name[:1]) + transliterate(second_name).lower()
    # генерируем пароль
    password = password_generator(8)
    # выводим данные по будующему пользователю
    print(transliterate(name) + u" " + transliterate(second_name) + u" " + username + u" " + password)
    # создаём пользователя
    user = User.objects.create_user(username=username, email=a[1], password=password)
    # присваиваем имя и фамилию
    user.first_name = name
    user.last_name = second_name
    # сохраняем пользователя
    user.save()
    # создаём студента на основе пользователя
    student = Student.objects.create(user=user, st_klass='10-3', st_group=a[2])
    student.save()

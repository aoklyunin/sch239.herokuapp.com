# coding=utf-8

from sworks.models import Student

arr = [ ['Абдурахманов Рауль',1],
        ['Бей Святослав',1],
        ['Берхман Евгений',1],
        ['Ведь Олеся',1],
        ['Винникова Анна',1],
        ['Вьюгинов Андрей',1],
        ['Грачев Иван',1],
        ['Грек Полина',1],
        ['Димитров Благой',1],
        ['Еремеев Иван',1],
        ['Звонов Даниил',1],
        ['Златковский Марк',1],
        ['Зорин Андрей',1],
        ['Иванова Марианна',1],
        ['Игнатьев Артур',2],
        ['Козар Илья',2],
        ['Котова Олеся',2],
        ['Лабес Алена',2],
        ['Мартыненко Анастасия',2],
        ['Никитин Михаил',2],
        ['Нургалиев Артём',2],
        ['Нургалиев Тимур',2],
        ['Попелышко Аким',2],
        ['Смирнов Даниил',2],
        ['Смирнов Михаил',2]]

for a in arr:
    s = Student(name=a[0],st_group=a[1],st_klass=9)
    s.save()


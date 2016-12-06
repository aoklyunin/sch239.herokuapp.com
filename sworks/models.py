# -*- coding: utf-8 -*-
# модели Django
from __future__ import unicode_literals

import datetime

from django.contrib.auth.models import User
from django.db import models


# тип работы: дома, в классе
class WorkType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


# тип работы: программирование, эссе
class TaskType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


# задание
class Task(models.Model):
    # имя задания
    task_name = models.CharField(max_length=200)
    # программирование/эссе
    task_type = models.ForeignKey(TaskType)
    # в классе/дома
    work_type = models.ForeignKey(WorkType)
    # кода выложено
    pub_date = models.DateField('date published')
    # список баллов на 1
    est1 = models.CharField(max_length=200)
    # список баллов на 2
    est2 = models.CharField(max_length=200)
    # список баллов на 3
    est3 = models.CharField(max_length=200)
    # список баллов на 4
    est4 = models.CharField(max_length=200)
    # список баллов на 5
    est5 = models.CharField(max_length=200)

    def __str__(self):
        return self.task_name + '(' + str(self.pub_date) + ')'

    def __unicode__(self):
        return self.task_name


# модель языка программирования
class CodeLanguage(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# модель программного кода
class ProgramCode(models.Model):
    class Meta:
        ordering = ['n']

    # язык программирования
    language = models.ForeignKey(CodeLanguage)
    # непосредственный код
    text = models.CharField(max_length=1000000)
    # номер (на всякий случай)
    n = models.IntegerField(default=0)
    # ссылка на исходный код
    link = models.CharField(max_length=1000,default="")

    def __str__(self):
        return str(self.n)+" : "+self.text.decode('utf-8')

    def __unicode__(self):
        return str(self.n)+" : "+self.text.decode('utf-8')

# оценка
class Mark(models.Model):
    # задание
    task = models.ForeignKey(Task)
    # оценка
    m_value = models.IntegerField(default=0)
    # дата добавления
    add_date = models.DateTimeField(default=datetime.datetime.now())
    # ссылка на работу
    link = models.CharField(max_length=200)
    # исходники
    sources = models.ManyToManyField(ProgramCode)
    # проверена ли оценка
    checked = models.IntegerField(default=0)

    def __str__(self):
        return self.task.task_name + '(' + str(self.add_date) + ') ' + str(self.m_value)

    def __unicode__(self):
        return self.task.task_name + '(' + str(self.add_date) + ' ' + str(self.m_value)


# класс студента
class Student(models.Model):
    # пользователь
    user = models.OneToOneField(User)
    # класс
    st_klass = models.CharField(max_length=200)
    # группа
    st_group = models.IntegerField()
    # оценки
    marks = models.ManyToManyField(Mark)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name + '(' + str(self.st_klass) + '.' + str(
            self.st_group) + ')'

    def __unicode__(self):
        return self.user.first_name + ' ' + self.user.last_name


# комментарий к попытке
class AttemptComment(models.Model):
    class Meta:
        ordering = ['-datetime']

    # прочитан или нет
    isReaded = models.BooleanField(default=False)
    # текст комментария
    text = models.CharField(max_length=2000)
    # автор комментария
    author = models.ForeignKey(Student)
    # дата написания
    datetime = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        return self.text

    def __unicode__(self):
        return self.text


# попытка
class Attempt(models.Model):
    class Meta:
        ordering = ['add_date']

    # кто оставил
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    # задание
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    # дата добавления
    add_date = models.DateTimeField(default=datetime.datetime.now())
    # ссылка
    link = models.CharField(max_length=200)
    # комментарии к попытке
    comment = models.ManyToManyField(AttemptComment)
    # состояние: 0 - не просмотрена, 1 - просмотрена, 2 - принята, 3 - отклонена
    state = models.IntegerField(default=0)

    def __str__(self):
        return self.student.__unicode__() + '(' + str(self.add_date) + ')'

    def __unicode__(self):
        return self.student.__unicode__() + '.' + self.task.task_name + '(' + str(self.add_date) + ')'


class PretendVal(models.Model):
    student = models.ForeignKey(Student,null=True)
    mark = models.ForeignKey(Mark,null=True)
    programCode = models.ForeignKey(ProgramCode,null=True)
    unique = models.FloatField(default=0)

    def __str__(self):
        return self.mark.__str__()

    def __unicode__(self):
        return self.mark.__unicode__()

class PretendToCheat(models.Model):
    vals  = models.ManyToManyField(PretendVal)
    task = models.ForeignKey(Task,null=True)
    state = models.IntegerField(default=0)
    n = models.IntegerField(default=0)

    def __unicode__(self):
        return self.task.__unicode__()

    def __str__(self):
        return self.task.__str__()
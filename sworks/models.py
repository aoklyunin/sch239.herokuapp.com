# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class Student(models.Model):
    user = models.OneToOneField(User)
    st_klass = models.IntegerField()
    st_group = models.IntegerField()

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name + '(' + str(self.st_klass) + '.' + str(
            self.st_group) + ')'

    def __unicode__(self):
        return self.user.first_name + ' ' + self.user.last_name


class Task(models.Model):
    task_name = models.CharField(max_length=200)
    task_type = models.IntegerField()
    work_type = models.IntegerField()
    pub_date = models.DateField('date published')
    est1 = models.CharField(max_length=200)
    est2 = models.CharField(max_length=200)
    est3 = models.CharField(max_length=200)
    est4 = models.CharField(max_length=200)
    est5 = models.CharField(max_length=200)

    def __str__(self):
        return self.task_name + '(' + str(self.pub_date) + ')'

    def __unicode__(self):
        return self.task_name


class AttemptComment(models.Model):
    isReaded = models.BooleanField()
    text = models.CharField(max_length=2000)
    author = models.ForeignKey(Student)

    def __str__(self):
        return self.student.name + '.' + self.task.task_name + '(' + str(self.add_date) + ')'

    def __unicode__(self):
        return self.student.name + '.' + self.task.task_name + '(' + str(self.add_date) + ')'


class Attempt(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    add_date = models.DateTimeField('date added')
    checked = models.BooleanField()
    link = models.CharField(max_length=200)
    comment = models.ManyToManyField(AttemptComment)

    def __str__(self):
        return self.student.name + '.' + self.task.task_name + '(' + str(self.add_date) + ')'

    def __unicode__(self):
        return self.student.name + '.' + self.task.task_name + '(' + str(self.add_date) + ')'

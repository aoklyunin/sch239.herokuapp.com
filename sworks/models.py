# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.contrib.auth.models import User
from django.db import models



class WorkType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

class TaskType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class Task(models.Model):
    task_name = models.CharField(max_length=200)
    task_type = models.ForeignKey(TaskType)
    work_type = models.ForeignKey(WorkType)
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



class Mark(models.Model):
    task = models.ForeignKey(Task)
    m_value = models.IntegerField(default=0)
    add_date = models.DateTimeField(default=datetime.datetime.now())
    link = models.CharField(max_length=200)

    def __str__(self):
        return  self.task.task_name + '(' + str(self.add_date) + ') '+str(self.m_value)


    def __unicode__(self):
        return  self.task.task_name + '(' + str(self.add_date) + ' '+str(self.m_value)

class Student(models.Model):
    user = models.OneToOneField(User)
    st_klass = models.CharField(max_length=200)
    st_group = models.IntegerField()
    marks = models.ManyToManyField(Mark)
    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name + '(' + str(self.st_klass) + '.' + str(
            self.st_group) + ')'

    def __unicode__(self):
        return self.user.first_name + ' ' + self.user.last_name



class AttemptComment(models.Model):
    class Meta:
        ordering = ['-datetime']
    isReaded = models.BooleanField(default=False)
    text = models.CharField(max_length=2000)
    author = models.ForeignKey(Student)
    datetime = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        return self.text

    def __unicode__(self):
        return self.text



class Attempt(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    add_date = models.DateTimeField(default=datetime.datetime.now())
    link = models.CharField(max_length=200)
    comment = models.ManyToManyField(AttemptComment)
    state = models.IntegerField(default=0)

    def __str__(self):
        return self.student.__unicode__()+ '(' + str(self.add_date) + ')'

    def __unicode__(self):
        return self.student.__unicode__() + '.' + self.task.task_name + '(' + str(self.add_date) + ')'

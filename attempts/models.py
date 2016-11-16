# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models



class Student(models.Model):
    st_klass = models.IntegerField()
    st_group = models.IntegerField()
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name + '(' + str(self.st_klass) + '.' + str(self.st_group) + ')'

    def __unicode__(self):
        return self.name


class Task(models.Model):
    task_name = models.CharField(max_length=200)
    task_type = models.IntegerField()
    work_type = models.IntegerField()
    pub_date = models.DateField('date published')

    def __str__(self):
        return self.task_name + '(' + str(self.pub_date) + ')'

    def __unicode__(self):
        return self.task_name



class Attempt(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    add_date = models.DateTimeField('date added')
    comment = models.CharField(max_length=2000)
    checked = models.BooleanField()
    link = models.CharField(max_length=200)

    def __str__(self):
        return self.student.name + '.' + self.task.task_name + '(' + str(self.add_date) + ')'

    def __unicode__(self):
        return self.student.name + '.' + self.task.task_name + '(' + str(self.add_date) + ')'

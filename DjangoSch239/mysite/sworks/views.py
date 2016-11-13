# -*- coding: utf-8 -*-

import datetime
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response

# -*- coding: utf-8 -*-
from django.template import RequestContext
from samba.dcerpc.security import standard_mapping

from .models import Student, Task, Attempt
from django.template import loader
from django import forms


class NameForm(forms.Form):
    student = forms.ModelChoiceField(queryset=Student.objects.all(), empty_label="Выберите ученика", label="")
    task = forms.ModelChoiceField(queryset=Task.objects.all(), empty_label="Выберите задание", label="")
    comment = forms.CharField(max_length=2000,
                              widget=forms.Textarea(attrs={'rows': 4, 'cols': 40, 'placeholder': 'Комментарий'}),
                              label="")
    link = forms.CharField(max_length=200,
                           widget=forms.Textarea(attrs={'rows': 1, 'cols': 40, 'placeholder': 'Ссылка'}), label="")


def attempt(request):
    student_list = Student.objects.order_by('name')
    task_list = Task.objects.order_by('-pub_date')
    template = 'sworks/attempt.html'
    context = {
        'student_list': student_list,
        'task_list': task_list,
        "form": NameForm()
    }
    return render(request, template, context)


def index(request):
    template = 'sworks/index.html'
    return render(request, template)


def addAttempt(request):
    form = NameForm(request.POST)
    if request.method == "POST" and form.is_valid():
        student = form.cleaned_data['student']
        task = form.cleaned_data['task']
        comment = form.cleaned_data['comment']
        link = form.cleaned_data['link']
        date = datetime.datetime.now().date()
        at = Attempt(student=student, task=task, comment=comment, add_date=date, link=link, checked=False)
        at.save()
        return succesAddTemplate(request)
    else:
        student_list = Student.objects.order_by('name')
        task_list = Task.objects.order_by('-pub_date')
        return render_to_response("sworks/attempt.html", {
            'student_list': student_list,
            'task_list': task_list,
            'form': form,
        })


def errorAddingTemolate(request):
    return HttpResponse("Error adding")


def detail(request, task_id):
    return HttpResponse("You're looking at question %s." % task_id)


def results(request, task_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % task_id)


def succesAddTemplate(request):
    return HttpResponseRedirect('/')


def attemptList(request):
    if request.user.is_authenticated():
        attempt_list = Attempt.objects.order_by('-add_date').filter(checked=False)
        template = 'sworks/attemptList.html'
        context = {
            'attempt_list': attempt_list,
        }
        return render(request, template, context)
    else:
        return HttpResponse("Ага, сейчас. Разбежался...")


def removeAttempt(request, attemptId):
    attempt = Attempt.objects.get(pk=attemptId)
    attempt.checked = True
    attempt.save()
    return HttpResponseRedirect('/attemptList')

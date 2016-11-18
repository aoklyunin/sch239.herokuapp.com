# -*- coding: utf-8 -*-
from .models import Student, Task, Attempt
import datetime
from django.contrib import auth
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django import forms


class NameForm(forms.Form):
    student = forms.ModelChoiceField(queryset=Student.objects.all(), empty_label="Выберите ученика", label="")
    task = forms.ModelChoiceField(queryset=Task.objects.all(), empty_label="Выберите задание", label="")
    comment = forms.CharField(max_length=2000,
                              widget=forms.Textarea(attrs={'rows': 4, 'cols': 40, 'placeholder': 'Комментарий'}),
                              label="")
    link = forms.CharField(max_length=200,
                           widget=forms.Textarea(attrs={'rows': 1, 'cols': 40, 'placeholder': 'Ссылка'}), label="")


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': 'Логин'}),
                               label="")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Логин'}), label="")

    widgets = {
        'password': forms.PasswordInput(),
    }

def register(request):
    student_list = Student.objects.order_by('name')
    task_list = Task.objects.order_by('-pub_date')
    template = 'sworks/register.html'
    context = {
    #    "form": RegisterForm()
    }
    return render(request, template, context)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")


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
    if request.method == "POST":
        if ("username" in request.POST) and ("password" in request.POST):
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            mutable = request.POST._mutable
            request.POST._mutable = True
            if user is not None and user.is_active:
                # Правильный пароль и пользователь "активен"
                auth.login(request, user)
                messages.success(request, "успешный вход")
            else:
                messages.error(request, "пара логин-пароль не найдена")
    template = 'sworks/index.html'
    context = {
        "user": request.user,
        "form": LoginForm(),
    }
    return render(request, template, context)


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

# -*- coding: utf-8 -*-
from bson import is_valid

from django.contrib.auth.models import User
from .models import Student, Task, Attempt
import datetime
from django.contrib import auth
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django import forms

from django.http import Http404, HttpResponseForbidden
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django.contrib.auth.hashers import (
    UNUSABLE_PASSWORD_PREFIX, identify_hasher,
)
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.forms.utils import flatatt
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.html import format_html, format_html_join
from django.utils.http import urlsafe_base64_encode
from django.utils.safestring import mark_safe
from django.utils.text import capfirst
from django.utils.translation import ugettext, ugettext_lazy as _
import unicodedata

from django.contrib.auth.forms import UserCreationForm


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


class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': 'mylogin'}),
                               label="Логин")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'rows': 1, 'cols': 20, 'placeholder': 'qwerty123'}),
                               label="Пароль")
    rep_password = forms.CharField(widget=forms.PasswordInput(attrs={'rows': 1, 'cols': 20, 'placeholder': 'qwerty123'}),
                                   label="Повторите пароль")
    schooler_class = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': '10-3'}),
                                     label="Класс")
    schooler_group = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': '1'}),
                                     label="номер группы")
    mail = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': 'example@gmail.com'}),
                           label="Адрес электронной почты")
    name = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': 'Иван'}), label="Имя")
    second_name = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': 'Иванов'}),
                                  label="Фамилия")


def register(request):
    if request.method == 'POST':
        print "request.POST %s" % request.POST
        form = RegisterForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["password"] != form.cleaned_data["rep_password"]:
                messages.error(request, "пароли не совпадают")
                data = {'username':form.cleaned_data["username"],
                        'schooler_class': form.cleaned_data["schooler_class"],
                        'schooler_group': form.cleaned_data["schooler_group"],
                        'mail': form.cleaned_data["mail"],
                        'name': form.cleaned_data["name"],
                        'second_name': form.cleaned_data["second_name"],
                        }
                return render(request, "sworks/register.html", {
                        'form': RegisterForm(initial=data),
                        'ins_form': LoginForm()
                })
            else:
                musername = form.cleaned_data["username"]
                schooler_class = form.cleaned_data["schooler_class"]
                schooler_group = form.cleaned_data["schooler_group"]
                mmail = form.cleaned_data["mail"]
                name = form.cleaned_data["name"]
                second_name = form.cleaned_data["second_name"]
                mpassword = form.cleaned_data["password"]
                #try:
                user = User.objects.create_user(username=musername,
                                                email=mmail,
                                                password=mpassword)
                if user:
                    user.first_name = name
                    user.last_name = second_name
                    user.save()
                    s = Student.objects.create(user = user,st_klass=schooler_class,st_group=schooler_group)
                    s.save()
                    return HttpResponseRedirect("/")
            #except:
            #        messages.error(request, "не получилось создать пользователя")
            #        data = {'username': form.cleaned_data["username"],
            #                'schooler_class': form.cleaned_data["schooler_class"],
            #                'schooler_group': form.cleaned_data["schooler_group"],
            #                'mail': form.cleaned_data["mail"],
            #                'name': form.cleaned_data["name"],
            #                'second_name': form.cleaned_data["second_name"],
            #                }
            #        return render(request, "sworks/register.html", {
            #            'form': RegisterForm(initial=data),
            #            'ins_form': LoginForm()
            #        })
        else:
            return HttpResponseRedirect("/register/")
    else:
        return render(request, "sworks/register.html", {
            'form': RegisterForm(),
            'login_form': LoginForm()
        })


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
        "login_form": LoginForm(),
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

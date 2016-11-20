# -*- coding: utf-8 -*-
from .models import Student, Task, Attempt, AttemptComment
import datetime
from django.contrib import auth
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django import forms
from django.contrib.auth.models import User


class AddAttemptForm(forms.Form):
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
    rep_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'rows': 1, 'cols': 20, 'placeholder': 'qwerty123'}),
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
                data = {'username': form.cleaned_data["username"],
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
                try:
                    user = User.objects.create_user(username=musername,
                                                    email=mmail,
                                                    password=mpassword)
                    if user:
                        user.first_name = name
                        user.last_name = second_name
                        user.save()
                        s = Student.objects.create(user=user, st_klass=schooler_class, st_group=schooler_group)
                        s.save()
                    return HttpResponseRedirect("/")
                except:
                    messages.error(request, "не получилось создать пользователя")
                    data = {'username': form.cleaned_data["username"],
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
            return HttpResponseRedirect("/register/")
    else:
        return render(request, "sworks/register.html", {
            'form': RegisterForm(),
            'login_form': LoginForm()
        })


def personal(request):
    student = Student.objects.get(user=request.user)
    at_list = Attempt.objects.filter(student=student)
    return render(request, "sworks/personal.html", {
        'login_form': LoginForm(),
        'attempt_list': at_list,

    })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")


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


def attempt(request, attempt_id):
    return render(request, "sworks/attempt.html", {
        "attempt": Attempt.objects.get(pk=attempt_id),
        "login_form": LoginForm(),
        "user": request.user,
    })


def addAttempt(request):
    if request.method == "POST":
        form = AddAttemptForm(request.POST)
        if form.is_valid():
            task = form.cleaned_data['task']
            comment = form.cleaned_data['comment']
            link = form.cleaned_data['link']
            date = datetime.datetime.now().date()
            student = Student.objects.get(user=request.user)
            comment_object = AttemptComment.objects.create(isReaded=False, text=comment, author=student)
            comment_object.save()
            at = Attempt(student=student, task=task, add_date=date, link=link, checked=False)
            at.save()
            at.comment.add(comment_object)
            return HttpResponseRedirect('../../personal/')

    task_list = Task.objects.order_by('-pub_date')
    return render(request, "sworks/addAttempt.html", {
        "task_list": task_list,
        "login_form": LoginForm(),
        "form": AddAttemptForm(),
        "user": request.user,
    })


def errorAddingTemolate(request):
    return HttpResponse("Error adding")


def detail(request, task_id):
    return HttpResponse("You're looking at question %s." % task_id)


def results(request, task_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % task_id)


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

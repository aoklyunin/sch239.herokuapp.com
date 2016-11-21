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


class AttemptForm(forms.Form):
    text = forms.CharField(max_length=200,
                           widget=forms.Textarea(attrs={'rows': 4, 'cols': 40, 'placeholder': 'Ссылка'}), label="")


class AddTaskForm(forms.Form):
    task_name = forms.CharField(max_length=200,
                                widget=forms.Textarea(attrs={'rows': 1, 'cols': 40, 'placeholder': 'название задания'}), label="Название задания ")
    task_type = forms.CharField(max_length=200,
                                widget=forms.Textarea(attrs={'rows': 1, 'cols': 40, 'placeholder': ''}), label="Классное/ДЗ")
    work_type = forms.CharField(max_length=200,
                                widget=forms.Textarea(attrs={'rows': 1, 'cols': 40, 'placeholder': ''}), label="Тип работы")
    pub_date = forms.CharField(max_length=200,
                               widget=forms.Textarea(attrs={'rows': 1, 'cols': 40, 'placeholder': ''}), label="Дата опубликовая")
    est1 = forms.CharField(max_length=200,
                           widget=forms.Textarea(attrs={'rows': 1, 'cols': 40, 'placeholder': ''}), label="Оценка 1")
    est2 = forms.CharField(max_length=200,
                           widget=forms.Textarea(attrs={'rows': 1, 'cols': 40, 'placeholder': ''}), label="Оценка 2")
    est3 = forms.CharField(max_length=200,
                           widget=forms.Textarea(attrs={'rows': 1, 'cols': 40, 'placeholder': ''}), label="Оценка 3")
    est4 = forms.CharField(max_length=200,
                           widget=forms.Textarea(attrs={'rows': 1, 'cols': 40, 'placeholder': ''}), label="Оценка 4")
    est5 = forms.CharField(max_length=200,
                           widget=forms.Textarea(attrs={'rows': 1, 'cols': 40, 'placeholder': ''}), label="Оценка 5")



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
                    messages.error(request, "Такой пользователь уже есть")
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
    at = Attempt.objects.get(id=attempt_id)
    if request.method == "POST":
        form = AttemptForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            student = Student.objects.get(user=request.user)
            comment_object = AttemptComment.objects.create(isReaded=False, text=text, author=student)
            comment_object.save()
            at.comment.add(comment_object)
    form = AttemptForm()
    return render(request, "sworks/attempt.html", {
        "attempt": at,
        "text_form": form,
        "login_form": LoginForm(),
        "user": request.user,
    })


def addTask(request):
    if request.method == "POST":
        form = AddTaskForm(request.POST)
        if form.is_valid():
            task_name = form.cleaned_data['task_name']
            task_type = form.cleaned_data['task_type']
            work_type = form.cleaned_data['work_type']
            pub_date = form.cleaned_data['pub_date']
            est1 = form.cleaned_data['est1']
            est2 = form.cleaned_data['est2']
            est3 = form.cleaned_data['est3']
            est4 = form.cleaned_data['est4']
            est5 = form.cleaned_data['est5']
            t = Task.objects.create(task_name = task_name, task_type =task_type,
                                    work_type=work_type,pub_date=pub_date,
                                    est1= est1, est2=est2,est3=est3,
                                    est4=est4,est5=est5)
            t.save()
    data = {
        'task_name':'',
        'task_type':0,
        'work_type':0,
        'pub_date':datetime.date.today(),
        'est1':'0,1,2',
        'est2':'3,4,5',
        'est3':'6,7,8',
        'est4':'10,9',
        'est5':'11'
    }

    return render(request, "sworks/addTask.html", {
        "task_form": AddTaskForm(initial=data),
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
            at = Attempt(student=student, task=task, add_date=date, link=link)
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

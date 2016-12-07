# -*- coding: utf-8 -*-
# модуль с формами
from django import forms

from sworks.models import Task, TaskType, WorkType


# форма добавления попытки
class AddAttemptForm(forms.Form):
    # задание
    task = forms.ModelChoiceField(queryset=Task.objects.all(), empty_label="Выберите задание", label="")
    # первый комментарий
    comment = forms.CharField(max_length=2000,
                              widget=forms.Textarea(attrs={'rows': 4, 'cols': 40, 'placeholder': 'Комментарий'}),
                              label="")
    # ссылка на попытку
    link = forms.CharField(max_length=200,
                           widget=forms.Textarea(attrs={'rows': 1, 'cols': 40, 'placeholder': 'Ссылка'}), label="")


# форма для просмотра своей попытки
class AttemptForm(forms.Form):
    text = forms.CharField(max_length=200,
                           widget=forms.Textarea(attrs={'rows': 4, 'cols': 40, 'placeholder': 'Ссылка'}), label="")


# форма добавления задания
class AddTaskForm(forms.Form):
    # имя задания
    task_name = forms.CharField(max_length=200,
                                widget=forms.Textarea(attrs={'rows': 1, 'cols': 40, 'placeholder': 'название задания'}),
                                label="Название задания ")
    # тип задания: программирование/эссе
    task_type = forms.ModelChoiceField(queryset=TaskType.objects.all(), initial=0)
    # тип работы: в классе/дома
    work_type = forms.ModelChoiceField(queryset=WorkType.objects.all(), initial=0)
    # дата выдачи
    pub_date = forms.CharField(max_length=200,
                               widget=forms.Textarea(attrs={'rows': 1, 'cols': 40, 'placeholder': ''}),
                               label="Дата опубликовая")
    # список баллов на оценку 1
    est1 = forms.CharField(max_length=200,
                           widget=forms.Textarea(attrs={'rows': 1, 'cols': 40, 'placeholder': ''}), label="Оценка 1")
    # список баллов на оценку 2
    est2 = forms.CharField(max_length=200,
                           widget=forms.Textarea(attrs={'rows': 1, 'cols': 40, 'placeholder': ''}), label="Оценка 2")
    # список баллов на оценку 3
    est3 = forms.CharField(max_length=200,
                           widget=forms.Textarea(attrs={'rows': 1, 'cols': 40, 'placeholder': ''}), label="Оценка 3")
    # список баллов на оценку 4
    est4 = forms.CharField(max_length=200,
                           widget=forms.Textarea(attrs={'rows': 1, 'cols': 40, 'placeholder': ''}), label="Оценка 4")
    # список баллов на оценку 5
    est5 = forms.CharField(max_length=200,
                           widget=forms.Textarea(attrs={'rows': 1, 'cols': 40, 'placeholder': ''}), label="Оценка 5")


# форма логина
class LoginForm(forms.Form):
    # имя пользователя
    username = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': 'Логин'}),
                               label="")
    # пароль
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}), label="")

    widgets = {
        'password': forms.PasswordInput(),
    }


# форма регистрации
class RegisterForm(forms.Form):
    # логин
    username = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': 'mylogin'}),
                               label="Логин")
    # пароль
    password = forms.CharField(widget=forms.PasswordInput(attrs={'rows': 1, 'cols': 20, 'placeholder': 'qwerty123'}),
                               label="Пароль")
    # повтор пароля
    rep_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'rows': 1, 'cols': 20, 'placeholder': 'qwerty123'}),
        label="Повторите пароль")
    # класс
    schooler_class = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': '10-3'}),
                                     label="Класс")
    # группа
    schooler_group = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': '1'}),
                                     label="номер группы")
    # почта
    mail = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': 'example@gmail.com'}),
                           label="Адрес электронной почты")
    # имя
    name = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': 'Иван'}), label="Имя")
    # фамилия
    second_name = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': 'Иванов'}),
                                  label="Фамилия")


# форма для оценки
class MarkForm(forms.Form):
    # оценка
    mark = forms.CharField(max_length=1,
                           widget=forms.Textarea(attrs={'rows': 1, 'cols': 2}),
                           label="")

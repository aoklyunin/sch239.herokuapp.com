# -*- coding: utf-8 -*-
from django import forms

from sworks.models import Task, TaskType, WorkType


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
                                widget=forms.Textarea(attrs={'rows': 1, 'cols': 40, 'placeholder': 'название задания'}),
                                label="Название задания ")

    task_type = forms.ModelChoiceField(queryset=TaskType.objects.all(), initial=0)
    work_type = forms.ModelChoiceField(queryset=WorkType.objects.all(), initial=0)

    pub_date = forms.CharField(max_length=200,
                               widget=forms.Textarea(attrs={'rows': 1, 'cols': 40, 'placeholder': ''}),
                               label="Дата опубликовая")
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
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}), label="")

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




class MarkForm(forms.Form):
    mark = forms.CharField(max_length=1,
                           widget=forms.Textarea(attrs={'rows': 1, 'cols': 1}),
                           label="")


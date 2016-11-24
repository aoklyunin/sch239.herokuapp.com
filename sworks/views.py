# -*- coding: utf-8 -*-
from django.views.decorators.csrf import csrf_exempt
from localCode.moodle import MoodleHelper
from .models import Student, Task, Attempt, AttemptComment, TaskType, WorkType, Mark
import datetime
from django.contrib import auth
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django import forms
from django.contrib.auth.models import User
from django.http import JsonResponse


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


def getValBySum(task, sum):
    s = str(round(sum))
    if s in task.est1:
        return int(1)
    elif s in task.est2:
        return int(2)
    elif s in task.est3:
        return int(3)
    elif s in task.est4:
        return int(4)
    elif s in task.est5:
        return int(5)
    else:
        return int(0)


def loadAttempt(request, taskName, taskType):
    moodle = MoodleHelper()
    lst = []
    attempts = moodle.loadAttempts(taskName, taskType == "Программирование")
    flg = False
    for at in attempts:
        user = User.objects.filter(first_name=at["name"], last_name=at["second_name"]).first()
        if user:
            student = Student.objects.filter(user=user).first()
            task = Task.objects.get(task_name=taskName)
            if student:
                m = student.marks.filter(task=task).first()
                if m:
                    if getValBySum(task, at["sum"]) > m.m_value:
                        m.m_value = getValBySum(task, at["sum"])
                        m.link = at["href"]
                else:
                    m = Mark.objects.create(task=task, m_value=getValBySum(task, at["sum"]), link=at["href"])
                m.save()
                student.marks.add(m)
            else:
                flg = True
                messages.error(request, "не найден студент " + at["name"] + " " + at["second_name"])
        else:
            flg = True
            messages.error(request, "не найден пользователь " + at["name"] + " " + at["second_name"])

    if len(lst) == 0 and not flg:
        return HttpResponseRedirect('../../../marks/')
    return render(request, "sworks/loadAttempt.html", {
        'lst': lst,
        'taskName': taskName,
        'taskType': taskType,
        "user": request.user,
    })


class markForm(forms.Form):
    mark = forms.CharField(max_length=1,
                           widget=forms.Textarea(attrs={'rows': 1, 'cols': 1}),
                           label="")


def markView(request, mark_id):
    m = Mark.objects.get(id=mark_id)
    form = markForm(initial={"mark": m.m_value})

    if request.method == "POST":
        form = markForm(request.POST)
        if form.is_valid():
            m.m_value = form.cleaned_data["mark"]
            m.save()

    s = Student.objects.filter(marks=m).first()
    moodle = MoodleHelper()
    arr = moodle.loadEssayAttempt('http://mdl.sch239.net/mod/quiz/review.php?attempt=16443')

    context = {
        "arr": arr,
        "student": s,
        "m": m,
        "user": request.user,
        "form": form,
    }
    return render(request, "sworks/markView.html", context)


class hrefClass():
    def __init__(self, href, text):
        self.href = href
        self.text = text


def marks(request):
    data = []
    tasks = Task.objects.filter(pub_date__gt=datetime.date.today() - datetime.timedelta(days=40)).order_by('pub_date')
    tasknames = []
    tasktypes = []
    for task in tasks:
        tasknames.append(task.task_name)
        tasktypes.append(task.task_type.name)

    for user in User.objects.all().order_by("last_name"):
        student = Student.objects.filter(user=user).first()
        if student:
            arr = []
            arr.append(hrefClass("", student.user.last_name + " " + student.user.first_name))
            dict = {}
            for mark in student.marks.all():
                dict[mark.task.task_name] = mark
            for task, ttype in zip(tasknames, tasktypes):
                if task in dict.keys():
                    href = "../../../markView/" + str(dict[task].id) + "/"
                    arr.append(hrefClass(href, dict[task].m_value))
                else:
                    arr.append(hrefClass("", 0))
            data.append(arr)
    context = {
        "data": data,
        "user": request.user,
        "tasks": tasks
    }
    return render(request, "sworks/marks.html", context)


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


@csrf_exempt
def getTasks(request):
    if request.method == "POST":
        if request.POST["begin_date"] or request.POST["end_date"]:
            pickup_records = []
            for task in Task.objects.all():
                record = {"pub_date": task.pub_date,
                          "task_name": task.task_name,
                          "task_type": task.task_type.name,
                          "work_type": task.work_type.name,
                          "est1": task.est1,
                          "est2": task.est2,
                          "est3": task.est3,
                          "est4": task.est4,
                          "est5": task.est5}
                pickup_records.append(record)
            return JsonResponse({'tasks': pickup_records}, safe=False)
        return JsonResponse({'error': 'нет параметров дат'}, safe=False)
    return JsonResponse({'error': 'не тот запрос'}, safe=False)


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
            t = Task.objects.create(task_name=task_name, task_type=task_type,
                                    work_type=work_type, pub_date=pub_date,
                                    est1=est1, est2=est2, est3=est3,
                                    est4=est4, est5=est5)
            t.save()
            messages.success(request, "Задание добавлено")

    data = {
        'task_name': '',
        'task_type': 'В классе',
        'work_type': "Программирование",
        'pub_date': datetime.date.today(),
        'est1': '0,1,2',
        'est2': '3,4,5',
        'est3': '6,7,8',
        'est4': '10,9',
        'est5': '11'
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

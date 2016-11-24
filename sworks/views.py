# -*- coding: utf-8 -*-
from django.views.decorators.csrf import csrf_exempt
from localCode.moodle import MoodleHelper
from sworks.forms import  LoginForm, AttemptForm, AddTaskForm, AddAttemptForm, MarkForm
from .models import Student, Task, Attempt, AttemptComment, Mark
import datetime
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.http import JsonResponse


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
        'login_form': LoginForm(),
    })



def markView(request, mark_id):
    m = Mark.objects.get(id=mark_id)
    form = MarkForm(initial={"mark": m.m_value})

    if request.method == "POST":
        form = MarkForm(request.POST)
        if form.is_valid():
            m.m_value = form.cleaned_data["mark"]
            m.save()

    s = Student.objects.filter(marks=m).first()
    moodle = MoodleHelper()
    arr = moodle.loadEssayAttempt(m.link)

    context = {
        "arr": arr,
        "student": s,
        "m": m,
        "user": request.user,
        "form": form,
        'login_form': LoginForm()
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
        "tasks": tasks,
        'login_form': LoginForm()
    }
    return render(request, "sworks/marks.html", context)


def personal(request):
    student = Student.objects.get(user=request.user)
    at_list = Attempt.objects.filter(student=student).order_by('-state')
    return render(request, "sworks/personal.html", {
        'login_form': LoginForm(),
        'attempt_list': at_list,

    })


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
        'est5': '11',
        'ins_form': LoginForm()
    }

    return render(request, "sworks/addTask.html", {
        "task_form": AddTaskForm(initial=data),
        "login_form": LoginForm(),
        "user": request.user
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
        attempt_list = Attempt.objects.order_by('-add_date').filter(state__range=[0,1])
        template = 'sworks/attemptList.html'
        markList = []
        for attempt in attempt_list:
            markList.append(Mark.objects.filter(task=attempt.task, student=attempt.student).first())
            if attempt.state == 0:
                attempt.state = 1
                attempt.save()
        context = {
            'arr': zip(attempt_list,markList)

        }
        return render(request, template, context)

def success(request,attempt_id):
    attempt = Attempt.objects.get(id = attempt_id)
    attempt.state = 2
    attempt.save()
    return HttpResponseRedirect('../../../attemptList/')
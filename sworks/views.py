# -*- coding: utf-8 -*-
import datetime

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from localCode.moodle import MoodleHelper
from sworks.forms import LoginForm, AttemptForm, AddTaskForm, AddAttemptForm, MarkForm
from .models import Student, Task, Attempt, AttemptComment, Mark, PretendToCheat, TaskType


# просмотр оценки
def markView(request, mark_id):
    # получаем оценку
    m = Mark.objects.get(id=mark_id)
    # в форму кладём изначально текущую оценку
    form = MarkForm(initial={"mark": m.m_value})
    # если post-запрос
    if request.method == "POST":
        # строим форму на основе post-запроса
        form = MarkForm(request.POST)
        if form.is_valid():
            # меняем оценку
            m.m_value = form.cleaned_data["mark"]
            m.save()
    # получаем студента, которому принадлежит оценка
    s = Student.objects.filter(marks=m).first()
    # получаем ссылки из попытки
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


# классы ссылки
class hrefClass():
    def __init__(self, href, text):
        self.href = href
        self.text = text


# журнал
def marks(request):
    # данные для журнала
    data = []
    # получаем все задания за последние 30 дней
    tasks = Task.objects.filter(pub_date__gt=datetime.date.today() - datetime.timedelta(days=15)).order_by('pub_date')
    # имена заданий
    tasknames = []
    # типы заданий
    tasktypes = []
    # для экономии ресурсов заранее получаем все типы и названия заданий
    for task in tasks:
        tasknames.append(task.task_name)
        tasktypes.append(task.task_type.name)
    # перебираем всех студентов
    for student in Student.objects.filter(st_klass="10-3").order_by("user__last_name"):
        # если студент существует
        if student:
            # строка журнала
            arr = []
            # добавляем ссылку с текстом "фамилия имя"
            arr.append(hrefClass("", student.user.last_name + " " + student.user.first_name))
            # делаем словарь для получения оценок
            dict = {}
            # перебираем оценки студента
            for mark in student.marks.all():
                # в качестве ключа используем имя задания
                dict[mark.task.task_name] = mark
            # перебираем имя и тип задания
            for task, ttype in zip(tasknames, tasktypes):
                # если у пользователя есть оценка
                if task in dict.keys():
                    # возвращаем ссылку на просмотр оценки с текстом самой оценки
                    href = "../../../markView/" + str(dict[task].id) + "/"
                    arr.append(hrefClass(href, dict[task].m_value))
                else:
                    # делаем пустую ссылку
                    arr.append(hrefClass("", 0))
            data.append(arr)

    context = {
        "data": data,
        "user": request.user,
        "tasks": tasks,
        'login_form': LoginForm()
    }
    return render(request, "sworks/marks.html", context)


# личный кабинет
def personal(request):
    # по пользователю получаем имя
    student = Student.objects.get(user=request.user)
    # список попыток, созданных текущем пользователем
    at_list = Attempt.objects.filter(student=student).order_by('-state')
    return render(request, "sworks/personal.html", {
        'login_form': LoginForm(),
        'attempt_list': at_list,
    })


# просмотр попытки по id
def attempt(request, attempt_id):
    # ищем попытку с заданным id
    at = Attempt.objects.get(id=attempt_id)
    # если пользователь хочет добавить комментарий
    if request.method == "POST":
        form = AttemptForm(request.POST)
        if form.is_valid():
            # текст комментария
            text = form.cleaned_data['text']
            # студент, написавший комментарий
            student = Student.objects.get(user=request.user)
            # создаём комментарий
            comment_object = AttemptComment.objects.create(isReaded=False, text=text, author=student)
            # сохраняем комментарий
            comment_object.save()
            at.comment.add(comment_object)
    form = AttemptForm()
    return render(request, "sworks/attempt.html", {
        "attempt": at,
        "text_form": form,
        "login_form": LoginForm(),
        "user": request.user,
    })


# организация обработки внешнего post-запроса
# для этого сделан декоратор @csrf_exempt
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


# добавление задания
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


# добавление попытки
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

    task_list = Task.objects.all().filter(pub_date__gt=datetime.date.today() - datetime.timedelta(days=30)).order_by(
        '-pub_date')
    return render(request, "sworks/addAttempt.html", {
        "task_list": task_list,
        "login_form": LoginForm(),
        "form": AddAttemptForm(),
        "user": request.user,
    })


# принятые попытки
def successAttemptList(request):
    if request.user.is_authenticated():
        attempt_list = Attempt.objects.order_by('-add_date').filter(state=2)
        template = 'sworks/attemptList.html'
        markList = []
        for attempt in attempt_list:
            markList.append(Mark.objects.filter(task=attempt.task, student=attempt.student).first())
            if attempt.state == 0:
                attempt.state = 1
                attempt.save()
        context = {
            'arr': zip(attempt_list, markList)
        }
        return render(request, template, context)


# необработанные попытки
def attemptList(request):
    if request.user.is_authenticated():
        attempt_list = Attempt.objects.order_by('-add_date').filter(state__range=[0, 1])
        template = 'sworks/attemptList.html'
        markList = []
        for attempt in attempt_list:
            markList.append(Mark.objects.filter(task=attempt.task, student=attempt.student).first())
            if attempt.state == 0:
                attempt.state = 1
                attempt.save()
        context = {
            'arr': zip(attempt_list, markList)

        }
        return render(request, template, context)


# принять попытку по id
def success(request, attempt_id):
    attempt = Attempt.objects.get(id=attempt_id)
    attempt.state = 2
    attempt.save()
    return HttpResponseRedirect('../../../attemptList/')


# отклонить попытку
def drop(request, attempt_id):
    attempt = Attempt.objects.get(id=attempt_id)
    attempt.state = 3
    attempt.save()
    return HttpResponseRedirect('../../../attemptList/')


def cheaters(request):
    template = 'sworks/cheaters.html'
    tt = TaskType.objects.get(name="Программирование")
    data = []
    for task in Task.objects.filter(task_type=tt).filter(pub_date__gt=datetime.date.today() - datetime.timedelta(days=15)):
        ps = PretendToCheat.objects.filter(task=task).filter(state=0)
        arr = []
        for p in ps:
            flg = False
            for val in p.vals.all():
                if val.mark.m_value!=-1:
                    flg = True
            if flg:
                arr.append(p)
        data.append([task.task_name,arr])
    context = {
        "data":data
    }
    return render(request, template, context)


def punishCheater(request, p_id):
    p = PretendToCheat.objects.get(pk = p_id)
    for val in p.vals.all():
        val.mark.m_value = -1
        val.mark.save()
    p.state = 1
    p.save()
    return HttpResponseRedirect("../../../../cheaters/")



def dropCheater(request,p_id):
    p = PretendToCheat.objects.get(pk=p_id)
    p.vals.all().delete()
    p.delete()
    return HttpResponseRedirect("../../../../cheaters/")

def punished(request):
    template = 'sworks/cheaters.html'
    tt = TaskType.objects.get(name="Программирование")
    data = []
    for task in Task.objects.filter(task_type=tt).filter(
            pub_date__gt=datetime.date.today() - datetime.timedelta(days=15)):
        ps = PretendToCheat.objects.filter(task=task).filter(state=1)
        data.append([task.task_name, ps])
    context = {
        "data": data
    }
    return render(request, template, context)
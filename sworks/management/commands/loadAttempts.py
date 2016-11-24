# coding=utf-8

from django.contrib.auth.models import User
from django.core.management import BaseCommand

from localCode.moodle import MoodleHelper
from sworks.models import Student, Task, Mark


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


class Command(BaseCommand):
    helf = 'load all attempts'

    def handle(self, *args, **options):
        moodle = MoodleHelper()
        lst = []
        for task in Task.objects.all():
            attempts = moodle.loadAttempts(task.task_name, task.task_type.name == "Программирование")
            for at in attempts:
                user = User.objects.filter(first_name=at["name"], last_name=at["second_name"]).first()
                if user:
                    student = Student.objects.filter(user=user).first()
                    if student:
                        m = student.marks.filter(task=task).first()
                        if m:
                            if getValBySum(task, at["sum"]) > m.m_value:
                                m.m_value = getValBySum(task, at["sum"])
                                m.link = at["href"]
                                m.save()
                        else:
                            m = Mark.objects.create(task=task, m_value=getValBySum(task, at["sum"]), link=at["href"])
                            m.save()
                            student.marks.add(m)

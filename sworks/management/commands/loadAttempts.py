# coding=utf-8
import datetime
from django.contrib.auth.models import User
from django.core.management import BaseCommand

from localCode.moodle import MoodleHelper
from sworks.models import Student, Task, Mark, TaskType


def getValBySum(task, sum):
    s = str(int(sum))
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
        #for task in Task.objects.filter(pub_date__gt=datetime.date.today() - datetime.timedelta(days=10)):
        for task in Task.objects.all():
            #print(task.task_name)
            try:
                tt = TaskType.objects.get(name= "Программирование")
                attempts = moodle.loadAttempts(task.task_name, task.task_type==tt)
                for at in attempts:
                   # print(at["second_name"]+" "+str(at["sum"]))
                    user = User.objects.filter(first_name=at["name"], last_name=at["second_name"]).first()
                    if user:
                        student = Student.objects.filter(user=user).first()
                        if student:
                            m = student.marks.filter(task=task).first()
                            #print(student.user.last_name+" "+str(m.m_value))
                            if m:
                              #  print(str(m.m_value)+" "+str(getValBySum(task, at["sum"])))
                                if getValBySum(task, at["sum"]) > m.m_value:
                                    m.m_value = getValBySum(task, at["sum"])
                                    m.link = at["href"]
                                    m.save()
                                #    print(student.user.username)
                            else:
                                m = Mark.objects.create(task=task, m_value=getValBySum(task, at["sum"]), link=at["href"])
                                m.save()
                                student.marks.add(m)

            except:
          #     print(" - ошибка загрузки:")
                pass
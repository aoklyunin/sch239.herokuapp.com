# coding=utf-8
# программа для загрузки оценок
import datetime

import itertools
from django.contrib.auth.models import User
from django.core.management import BaseCommand

from localCode.codeAnalysis import SimpleCodeAnalysis
from localCode.moodle import MoodleHelper
from sworks.models import Student, Task, Mark, TaskType, ProgramCode, CodeLanguage, PretendVal, PretendToCheat


# описание класса програмы
class Command(BaseCommand):
    # получаем двумерный массив первая координата - оценка, вторая - номер программы в оценке
    # возвращает массив и длину строк в нём
    def generateCodeDataFromMarks(self, marks):
        data = []
        ln = 0
        for m in marks:
            # m.checked = True
            # m.save()
            ar = []
            for source in m.sources.all():
                ar.append(SimpleCodeAnalysis(source))
            l = len(ar)
            if ln == 0 and l != 0:
                ln = l
            data.append(ar)
        # если программных кодов нет, то заполняем исходники пустыми строками
        for d in data:
            if (len(d)) == 0:
                for i in range(ln):
                    d.append(
                        SimpleCodeAnalysis(ProgramCode.objects.create(language=CodeLanguage.objects.all().first(),
                                                                      text="")))
        return (data, ln)

    # описание программы
    helf = 'checkCodes'

    def handle(self, *args, **options):
        # экземпляр класса для работы с mdl
        moodle = MoodleHelper()
        # проходим по всем заданиям за последние 30 дней

        tt = TaskType.objects.get(name="Программирование")
        for task in Task.objects.filter(task_type=tt).filter(
                pub_date__gt=datetime.date.today() - datetime.timedelta(days=30)):
            # for task in Task.objects.all():
            print(task.task_name)
            # try:
            marks = Mark.objects.filter(checked=0).filter(task=task)
            # print(marks)
            (add_data, ln) = self.generateCodeDataFromMarks(marks)
            if (len(add_data) == 0):
                print "в этом задании нет непроверенных оценок"
                continue
            marks.update(checked=1)
            # надо добавить фильтр по непроверенным оценкам
            marks = Mark.objects.filter(task=task)
            (all_data, ln) = self.generateCodeDataFromMarks(marks)

            for i in range(ln):
                arr = []
                for j in range(len(all_data)):
                    arr.append(all_data[j][i])
                arr_add = []
                for j in range(len(add_data)):
                    arr_add.append(add_data[j][i])
                dict = {}
                lstAdd = []
                for a, b in itertools.product(arr_add, arr):
                    if a.sorceCode != b.sorceCode:
                        c = a.compaireTo(b)
                        # print(c)

                        if c > 80:
                            if a in dict:
                                dict[a].append([b, c, i])
                            elif b in dict:
                                dict[b].append([a, c, i])
                            else:
                                dict[a] = [[b, c, i]]
                                lstAdd.append(b)

                for key, value in dict.iteritems():
                    print "begin"
                    m1 = Mark.objects.filter(sources=key.sorceCode).first()
                    print (key.sorceCode.link)
                    student = Student.objects.filter(marks=m1).first()
                    mainP = PretendVal.objects.create(programCode=key.sorceCode, mark=m1, student=student)
                    mainP.save()

                    pVal = PretendToCheat.objects.create(task=task, state=0, n=value[0][2])
                    pVal.save()
                    pVal.vals.add(mainP)
                    for v in value:
                        m2 = Mark.objects.filter(sources=v[0].sorceCode).first()
                        student = Student.objects.filter(marks=m2).first()
                        p = PretendVal.objects.create(student=student, mark=m2, programCode=v[0].sorceCode)
                        p.unique = v[1]
                        p.save()
                        pVal.vals.add(p)
                        print (v[0].sorceCode.link)
                    print "end"
                    # for d in data:
                    #   print(len(d[0]))



                    # except:
                    #    pass

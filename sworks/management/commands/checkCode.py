# coding=utf-8
# программа для загрузки оценок
import datetime

import itertools
from django.contrib.auth.models import User
from django.core.management import BaseCommand

from localCode.codeAnalysis import SimpleCodeAnalysis
from localCode.moodle import MoodleHelper
from sworks.models import Student, Task, Mark, TaskType, ProgramCode, CodeLanguage


# описание класса програмы
class Command(BaseCommand):
    # описание программы
    helf = 'checkCodes'

    def handle(self, *args, **options):
        # экземпляр класса для работы с mdl
        moodle = MoodleHelper()
        # проходим по всем заданиям за последние 30 дней
        tt = TaskType.objects.get(name="Программирование")
        for task in Task.objects.filter(task_type=tt).filter(pub_date__gt=datetime.date.today() - datetime.timedelta(days=30)):
            # for task in Task.objects.all():
                print(task.task_name)
            #try:
                marks = Mark.objects.filter(task = task)
                data = []
                ln = 0
                for m in marks:
                    ar = []
                    for source in m.sources.all():
                        ar.append(SimpleCodeAnalysis(source))
                    l = len(ar)
                    if ln==0 and l!= 0:
                        ln = l
                    data.append([ar,m])

                for d in data:
                    if (len(d[0]))==0:
                        for i in range(ln):
                            d[0].append(SimpleCodeAnalysis(ProgramCode.objects.create(language=CodeLanguage.objects.all().first(),
                                                                                      text = ""  )))

                for i in range(ln):
                    arr = []
                    for j in range(len(data)):
                        arr.append(data[j][0][i])
                    #print (arr)
                    dict = {}
                    for a,b in itertools.combinations(arr,2):
                            c = a.compaireTo(b)
                            #print(c)
                            if c>85:
                                if a in dict:
                                    dict[a].append([b,c,i])
                                elif b in dict:
                                    dict[b].append([a,c,i])
                                else:
                                    dict[a]=[[b,c,i]]
                                #print(c,i)
                                #m1 = Mark.objects.filter(sources=a.sorceCode).first()
                                #m2 = Mark.objects.filter(sources=b.sorceCode).first()
                                #print (m1.link)
                                #print (m2.link)
                                #print (a.canonizedText,b.canonizedText)
                    for key,value in dict.iteritems():
                        m1 = Mark.objects.filter(sources=key.sorceCode).first()
                        print ("lol")
                        print (m1.link)
                        for v in value:
                            print (v[1],v[2])
                            m2 = Mark.objects.filter(sources=v[0].sorceCode).first()
                            print (m2.link)
                #for d in data:
                 #   print(len(d[0]))



            #except:
            #    pass

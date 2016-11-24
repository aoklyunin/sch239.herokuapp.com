# coding=utf-8
import re
from operator import itemgetter

import requests
from lxml import html
from datetime import datetime

class MoodleHelper():
    MAX_RETRIES = 20
    # конструктор
    def __init__(self):
        self.session = requests.Session()
        self.adapter = requests.adapters.HTTPAdapter(max_retries=self.MAX_RETRIES)
        self.session.mount('https://', self.adapter)
        self.session.mount('http://', self.adapter)

        payload = {'username': 'kluninao', 'password': 'kluninao'}
        r = self.session.post('http://mdl.sch239.net/login/index.php', data=payload)
    # загружаем страницу по ссылке
    def loadUrl(self, url):
        response = self.session.get(url)
        return response
    # загружаем готовую к парсингу страницу
    def loadUrlParsed(self,url):
        response = self.session.get(url)
        return  html.document_fromstring(response.text)
    def loadAttempts(self,attempt_name,flgCode):
        # загружаем раздел
        page = self.loadUrlParsed('http://mdl.sch239.net/course/view.php?id=44')
        # ищем ссылку с нужным нам текстом (по факту там не просто текст
        # он обёрнут в <span>
        #print(attempt_name)
        try:
            at_span = page.xpath("//a/span[text()='"+attempt_name+"']")[0]
        except:
            return []
        # получаем непосредственно ссылку
        at_href = at_span.getparent().get("href")
        # загружаем страницу теста
        page = self.loadUrlParsed(at_href)
        # получаем ссылку на попытки
        at_href = page.xpath("//*[@class='quizattemptcounts']")[0].getchildren()[0].get("href")
        # загружаем попытки
        page = self.loadUrlParsed(at_href)
        # загружаем строки таблицы попыток
        trs = page.xpath("//*[@id='attempts']/tbody/tr")[:-3]
        # массив попыток
        arr = []
        for tr in trs:
            try:
                # словарь попытки
                dict = {}
                # поолучаем строку таблицы
                tds = tr.getchildren()
                # получаем ячейку с ссылкой и именем
                hrLst = tds[1].getchildren()
                # получаем имя фамилию
                name = hrLst[0].text
                # разворачиваем имя
                n = name.split(' ')
                # добавляем в словарь имя
                dict["name"] = n[0]
                dict["second_name"] = n[1]
                # добавляем в словарь ссылку на попытку
                dict["href"] = hrLst[2].get("href")
                # если это задача на программирование
                if flgCode:
                    # считаем сумму
                    sum = 0
                    for td in tds[8:]:
                        try:
                            s = td.getchildren()[0].getchildren()[0].getchildren()[1].text
                        except:
                            s = td.getchildren()[0].getchildren()[0].getchildren()[0].text
                        finally:
                            s = s.replace(',', '.')
                            # print(s)
                            sum += 0 if (s == "-" or float(s) < 0.1) else 1
                    dict["sum"] = sum
                    try:
                        dict["ev"] =  float(tds[7].getchildren()[0].text.replace(',', '.'))
                    except:
                        dict["ev"] = 0
                else:
                    dict["sum"] = 0
                    dict["ev"] = 0

                dict["mail"] = tds[2].text
                dict["state"]  = tds[3].text
                dict["date_started"]  = datetime.strptime( tds[4].text, "%d %B %Y %H:%M")
                dict["date_ended"] = datetime.strptime( tds[5].text, "%d %B %Y %H:%M") if tds[5].text!="-" else datetime.now()

                arr.append(dict)
            except:
                pass
        arr = sorted(arr,key=itemgetter("name"))
        return arr

    def loadEssayAttempt(self,link):
        page = self.loadUrlParsed(link)
        links = page.xpath("//*[@id=\"mod_quiz_navblock\"]/div[2]/div[1]/a")
        hrefs = []
        for l in links:
            href = l.get('href')
            if href.find('http')!=-1:
                hrefs.append(href)
        hrefs.append(link)
        arr = []
        for href in hrefs:
            page = self.loadUrlParsed(href)
            lst = page.xpath("//div[@class='ablock']/div/div/p")
            s = ""
            for l in lst:
                ar = []
                for r in re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', l.text):
                    ar.append(r)
                arr.append(ar)
        return arr


# coding=utf-8
# модуль для анализа программных кодов на списывание
import re
from collections import defaultdict

from localCode.constants import *
from sworks.models import ProgramCode

# по идее можно использоват Node
# from lib2to3.pytree import Node
# root = Node("")

# класс для работы с деревьями
# http://stackoverflow.com/questions/3009935/looking-for-a-good-python-tree-data-structure/12260480#12260480
# добавлять элементы можно
# a = tree()
# a["asfa"]=5
# a["asfa"]["a"] = 6
def tree(): return defaultdict(tree)


# Класс, соотв. лексеме
class Lex():
    # конструктор
    def __init__(self, rex, val):
        self.rex = rex
        self.val = val

class SimpleCodeAnalysis:
    text = ""
    canonizedText = ""
    root = tree()
    sorceCode = ProgramCode()
    # делаем исходный текст удобным для анализа
    def canonize(self,text):
        # убираем все лишние пробелы и переносы строк
        text = re.sub("\s+", " ", text)
        # убираем импорты за ненадобностью
        text = re.sub("import(.*?);", "", text)
        # убираем пробелы в начале и в конце текста
        text = text.strip()
        # убираем пробелы в примитивных конструкциях
        for s in STOP_SYMBOLS:
            text = text.replace(s+" ",s)
            text = text.replace(" "+s,s)

        for s in REPLACE_WORDS:
            text = text.replace(s[0],s[1])

        # убираем все лишние пробелы и переносы строк
        text = re.sub("\s+", " ", text)
        return text

    # формируем шилнгл по тексту
    def genshingle(self,source):
        import binascii
        shingleLen = 5  # длина шингла
        out = []
        for i in range(len(source) - (shingleLen - 1)):
            out.append(binascii.crc32(' '.join([x for x in source[i:i + shingleLen]]).encode('utf-8')))

        return out
    # сравниваем две даты с шинглами
    def compaireTo(self, source2):
        same = 0
        for i in range(len(self.shingledData)):
            if self.shingledData[i] in source2.shingledData:
                same = same + 1
        if len(self.shingledData)==0 or len(source2.shingledData)==0:
            return 0
        return same * 2 / float(len(self.shingledData) + len(source2.shingledData)) * 100

    def __init__(self, code):
        self.sorceCode = code
        # запускаем парсинг всего текста, с главным элементом в качестве корня
        self.text = self.sorceCode.text
        self.canonizedText = self.canonize(self.text)
        self.shingledData = self.genshingle(self.canonizedText)

    def printStruct(self):

        pass


# Класс анализатора кода
class CodeAnalysis:
    # корень дерева
    root = tree()
    # из текста выковыривает сождержимое скобок - это val,
    # и возвращается оставшийся текст
    def getTextFromBrackets(self, text):
        # выводим, чтобы понять, что обрабатываются скобки
        print("brackets")
        # разность между открывающими и закрывающими скобками
        cnt = 1
        # находим открывающий символ
        chr = text[0]
        # по открывающему симвуолу находим закрывающий
        chrClose = "}" if '{' == chr else ")"
        # идекс обхода
        pos = 1
        # пока открывающих скобок больше, чем закрывающих
        while cnt > 0:
            # изменяем разность скобок, если символ - скобка
            if text[pos] == chr: cnt += 1
            if text[pos] == chrClose: cnt -= 1
            pos += 1
        return (text[0:pos - 1], text[pos + 1:])

    # проверяем, что строка начинается с заданной регулярки
    def getTexFromRe(self, r, text):
        try:
            # проверка, что строка начинается с регуярки
            m = re.match(r[0], text)
            # если найдена
            if m:
                # получаем текст строки, отв. регулярке
                val = m.group(0)
                # удаляем из текеста эту строку
                text = text[len(val):]
                # вызываем лямбда-выражение для найденной лексемы
                val = r[1](val)
                # флаг, нужно вызывать разбор текста лексемы или нет
                flgRecurs = r[2]
                # вывдоим регулярку
                print(r)
                # говорим, что нашли лексему
                flg = True
        except:
            val = ""
            text = ""
            flgRecurs = False
            flg = False
        return (val, text, flgRecurs, flg)

    # парсим текст, аргументы: текст для разбора и корень, к которому присоединять все распарсенные элементы
    def parceText(self, text, root):
        # флаг, отвечающий, найдена ли хотя бы оддна лексема
        flg = True
        # пока находится хотя бы одна лексема и текст ненулевой
        while (flg) and (len(text) > 0):
            # считаем, что ни одной лексемы изначально не найдено
            flg = False
            # удаляем лишние пробелы в наале и конце текста
            text = text.strip()
            # текст лексемы
            val = ""
            # флаг, нужно ли вызывать обработчик для текста лексемы
            flgRecurs = False
            # ищем парные скобки
            for r in [C_DOUBLE_BRACKET, S_DOUBLE_BRACKET, R_DOUBLE_BRACKET]:
                if not flg:
                    (val, text, flgRecurs, flg) = self.getTexFromRe(r, text)
            # если первый символ строки равен "=",
            if not flg and text[0] == "=":
                # говорим, что нашли лексему
                flg = True
                # текст лексемы пустой
                val = ""
                # обрезаем текст
                text = text[1:]
            # если строка начинется с new
            if not flg and text.startswith("new"):
                # говорим, что нашли лексему
                flg = True
                # текст лексемы пустой
                val = ""
                # обрезаем текст
                text = text[3:]
            # если строка начинается с открывающейся скобки
            if not flg and text[0] == "{" or text[0] == "(":
                # получаем текст лексемы и оставшийся текст
                (val, text) = self.getTextFromBrackets(text)
                # говорим, что нашли лексему
                flg = True
                # говорим, что надо запускать рекурентный вызов для текста лексемы
                flgRecurs = True
            # проходим по всем регулярным выражениям
            for r in REGEX:
                if not flg:
                    (val, text, flgRecurs, flg) = self.getTexFromRe(r, text)
            # выводим текст лексемы
            print("val: " + val)
            # удаляем лишние пробелы в начале и конце оставшегося текста
            text = text.strip()
            # выводим оставшийся текст
            print("r_text: " + text)
            # если нужно разобрать содержимое лексемы
            if flg and flgRecurs:
                # вызываем её разбор
                self.parceText(val, root)

    def __init__(self, text):
        # убираем все лишние пробелы и переносы строк
        text = re.sub("\s+", " ", text)
        # запускаем парсинг всего текста, с главным элементом в качестве корня
        self.parceText(text, self.root)


#ca = SimpleCodeAnalysis(code_text2,0)
#cb = SimpleCodeAnalysis(code_text3,0)
#print(ca.compaireTo(cb))
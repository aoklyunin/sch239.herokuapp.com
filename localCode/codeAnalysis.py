# coding=utf-8
import re
from collections import defaultdict
from lib2to3.pytree import Node

from localCode.constants import *

def tree(): return defaultdict(tree)

class Lex():
    # конструктор
    def __init__(self, rex, val):
        self.rex = rex
        self.val = val

class CodeAnalysis:
    #root = Node("")
    # конструктор
    root = tree()

    # из текста выковыривает сождержимое скобок - это val,
    # и возвращается оставшийся текст
    def getTextFromBrackets(self,text):
        print("brackets")
        cnt = 1
        chr = text[0]

        chrClose = "}" if '{' == chr else ")"

        text = text[1:]
        pos = 1
        while cnt>0:
            if text[pos]==chr: cnt+=1
            if text[pos]==chrClose: cnt-=1
            pos+=1
        return (text[0:pos-1],text[pos+1:])

    def parceText(self,text,root):
        flg = True
        while (flg)and(len(text)>0):
            flg = False
            text = text.strip()
            val = ""

            for r in [C_DOUBLE_BRACKET,S_DOUBLE_BRACKET,R_DOUBLE_BRACKET]:
                if not flg:
                    try:
                        m = re.match(r[0], text)
                        if m:
                            val = m.group(0)
                            text = text[len(val):]
                            val = r[1](val)
                            flgRecurs = r[2]
                            print(r)
                            flg = True
                    except:
                        pass

            if text[0]=="=":
                flg = True
                val = ""
                text = text[1:]
            if text.startswith("new"):
                flg = True
                val = ""
                text = text[3:]
            if text[0] == "{" or text[0] == "(" :
                (val, text) = self.getTextFromBrackets(text)
                flg = True
                flgRecurs = True

            for r in REGEX:
                if not flg:
                    try:
                        m = re.match(r[0], text)
                        if m:
                            val = m.group(0)
                            text = text[len(val):]
                            val = r[1](val)
                            flgRecurs = r[2]
                            print(r)
                            flg = True
                    except:
                        pass

            print("val: "+val)
            text = text.strip()
            print("r_text: "+text)
            if flg and flgRecurs:
                self.parceText(val,root)


    def __init__(self,text):
        # убираем все лишние пробелы и переносы строк
        text = re.sub("\s+"," ",text)
        self.parceText(text,self.root)



# coding=utf-8
# В этом файлике лежат регулярные выражения, соответствующие лексемам java
R_IMPORT=["import(.*?);",lambda s:s[len("import"):-1].strip(),False,"import"]
R_PUBLIC = ["public",lambda s:s[len("public"):].strip(),False,"public"]
R_STATIC = ["static",lambda s:s[len("static"):].strip(),False,"static"]
R_CLASS = ["class",lambda s:s[len("class"):].strip(),False,"class"]
# самые распространённые лексемы
R_BACE_TYPES = "(void|byte|Byte|short|Short|int|Integer|long|Long|char|Character|float|Float|double|Double|String|StringBuilder|StringBuffer)"
R_SPACE_AND_LN_ONE_OR_MORE = "\s+"
R_ANY_COUNT_OF_ANY_SYMBOL = "(.*?)"
# коллекции
R_HASH_TABLE = "Hashtable < ?(.*?) ?, ?(.*?) ?>"
R_HASH_MAP = "HashMap ?< ?(.*?) ?, ?(.*?) ?>"
R_LINKED_HASH_MAP = "LinkedHashMap ?< ?(.*?) ?, ?(.*?) ?>"
R_TREE_MAP = "TreeMap ?< ?(.*?) ?, ?(.*?) ?>"
R_WEAK_HASH_MAP = "WeakHashMap ?< ?(.*?) ?, ?(.*?) ?>"
R_VECTOR = "Vector ?< ?(.*?) ?>"
R_STACK = "Stack ?< ?(.*?) ?>"
R_LINKED_LIST = "LinkedList ?< ?(.*?) ?>"
R_HASH_SET = "HashSet ?< ?(.*?) ?>"
R_LINKED_HASH_SET = "LinkedHashSet ?< ?(.*?) ?>"
R_TREE_SET = "TreeSet ?< ?(.*?) ?>"
R_PRIORITY_QUEQUE = "PriorityQueue ?< ?(.*?) ?>"
R_ARRAY_DEQUE = "ArrayDeque ?< ?(.*?) ?>"

R_COLLECTIONS = "(" + R_HASH_TABLE + "|" + R_HASH_MAP + "|" + R_LINKED_HASH_MAP + "|" + R_TREE_MAP + "|" + R_WEAK_HASH_MAP + "|" + R_VECTOR + "|" + R_STACK + "|" + R_LINKED_LIST + "|" + R_HASH_SET + "|" + R_LINKED_HASH_SET + "|" + R_TREE_SET + "|" + R_PRIORITY_QUEQUE + "|" + R_ARRAY_DEQUE + ")"

R_TYPES = [ R_COLLECTIONS[:-1]+"|"+R_BACE_TYPES[1:-1]+")",lambda s:s,False,"type"]

R_VAR_NAME = ["[a-zA-Z0-9]+",lambda s:s,False,"varName"]
R_VALUE = "(-?[0-9]+.?[0-9]*|((\"|\')(.*?)(\"|\'))"
R_VAR_DEFINITION = R_TYPES[0]+" "+R_VAR_NAME[0]+" ?;"
R_ASSIGNMENT = " (.*?) ?= ?(.*?) ?;"
R_VAR_DEFINITION_WITH_ASSIGNMENT = R_VAR_DEFINITION[:-1]+" ?= ?(.*?);"
R_VAR_ASSIGNMENT = R_VAR_NAME[0]+" ?= ?(.*?);"
R_ARGUMENTS = "(\((.*?)\))+"
R_CALL_METHOD = ["\.[a-zA-Z0-9]+",lambda s:s,False,"callMethod"]

R_METHOD_DEFENITION = R_TYPES[0][1:]+"|void)"+" "+R_VAR_NAME[0]+" ?"+R_ARGUMENTS+" ?{(.*?)}"

C_DOUBLE_BRACKET = ["\{\}",lambda s:s,False,"courly_bracket"]
S_DOUBLE_BRACKET = ["\[\]",lambda s:s,False,"square_bracket"]
R_DOUBLE_BRACKET = ["\(\)",lambda s:s,False,"round_bracket"]

STOP_SYMBOLS = [
    ",", "=", "+", "-", "/", "^", "!", "[", "]", "{", "}","(",")","&","|","<",">",";"
]
REPLACE_WORDS = [
    ["public",""],
    ["static",""],
    ["void main(String [] args)",""],
    ["System.out.",""],
    ["class(.*?){",""],
    ["Scanner(.*?)=new Scanner(System.in)",""],
    ["(",""],
    ["{",""],
    [")",""],
    ["}",""],
    ["//(.*?)\n",""],
    ["/*(.*?)*/",""]
]

# программный код для тестового рабора исходника на лексемы
code_text = """import java.util.Scanner

 ;import java.io.BufferedReader;
import   java.io.FileReader;

   import
                     java.io.FileWriter;
import java.io.IOException;
       import
         java.util.Random;
import



java.util.Scanner;

public

class     msc

{
    public
     static void main(String[]                       arge) {

           Scanner sc = new Scanner(System.in)

           ;
        float
         a =
          sc.nextFloat()   ;

        float
         b
         =
         sc.nextFloat(    )                ;
        if            ((a ==    b) && (a    == 0)) {

    System.out.println("any x"    )   ;
           }
        if ((a == b) &&

         ((a > 0) || (a        <        0))) {
            System.out.println("-1.0 " + "1.0");
        }

    if (     ((   b == 0) && ((a > b) || (a <     b)     ))    ) {
            System.out.println(0.0        );
        }
        if ((a!=0)&&(b!=0)&&  (a!=b)   && (b%a    ==        0) &&  (b   /   a>0   )   ) {
            double x = b / a;
            System.out.printf("%.1f", -x);
            System.out.print(" ");
            System.out.printf("%.1f", x);
        }
        if (((a == 0) && (a!=b))) {
            System.out.println("no such x");
        }
        if ((a!=0)&&(b!=0)&&(b%a!=0)&&(b/a>0)) {
            System.out.println("no such x");
        }
        if ((a!=0)&&(b!=0)&&(b/a<0)) {
            System.out.println("no such x");
        }
    }
}"""

code_text2 = """

import java.util.Scanner;
public class msc {

    public              static void main(String[] arge) {
        Scanner sc =            new Scanner(System.in);
        int n  =         sc.nextInt()     ;
        int m = sc.nextInt();
        int    l = 0;
        for (int i = 0; i<2; i++) {
            l = m*n;
        }
        System.out.println(l);
    }
}
"""

code_text3="""
import              java.util.Scanner;
public            class msc                {
    public static void main(String[] arge) {
        Scanner            sc = new Scanner(System.in);
        int n = sc.nextInt();
                int cnt =           0;
        n = n * 10;

        for (int i = 0; n >= 10; i++) {
            n = n / 10;
            cnt++;
        }
        System.out.println(cnt);
    }
}
"""


code_text4 = """
import java.util.Scanner        ;
public class msc {

    public static void main(String[] arge) {
        Scanner        sc = new Scanner(System.in);
        float         a = sc.nextFloat();
        float b      = sc.nextFloat();
        if ((a == b) && (a == 0)) {
            System.out.println("any x");
        }

        if ((a == b) && ((a > 0) || (a < 0))) {
            System.out.println("-1.0 " + "1.0");
        }
        if (((b == 0) && ((a > b) || (a < b)))) {
            System.out.println(0.0);
        }
        if ((a!=0)&&(b!=0)&&(a!=b)&&(b%a==0)&&(b/a>0)) {
            double x = b / a;
            System.out.printf("%.1f", -x);
            System.out.print(" ");
            System.out.printf("%.1f", x);
        }
        if (((a == 0) && (a!=b))) {
            System.out.println("no such x");
        }
        if ((a!=0)&&(b!=0)&&(b%a!=0)&&(b/a>0)) {
            System.out.println("no such x");
        }
        if ((a!=0)&&(b!=0)&&(b/a<0)) {
            System.out.println("no such x");
        }
    }
}
"""

# список регулярок для поиска лексем
REGEX = [
R_IMPORT,
R_CLASS ,
R_PUBLIC ,
R_STATIC,
R_CALL_METHOD,
R_TYPES,
R_VAR_DEFINITION,
R_ASSIGNMENT,
R_VAR_DEFINITION_WITH_ASSIGNMENT,
R_VAR_ASSIGNMENT,
R_ARGUMENTS,
R_VAR_NAME]

#!/usr/bin/python3
#from Stack import *

def Operator(INFExp):
        INFArr = StrToArr(INFExp);
        POSExp = InfxPosxConverter(INFArr);
        PosEv = Ev(POSExp);
        return(PosEv);

def StrToArr(INFStr):
    ArrToSpl = "";
    for i in INFStr:
        if(i == '('):
            ArrToSpl = ArrToSpl + ' ( ';
        elif(i == ')'):
            ArrToSpl = ArrToSpl + ' ) ';
        elif(i == '*'):
            ArrToSpl = ArrToSpl + ' * ';
        elif(i == '/'):
            ArrToSpl = ArrToSpl + ' / ';
        elif(i == '+'):
            ArrToSpl = ArrToSpl + ' + ';
        elif(i == '-'):
            ArrToSpl = ArrToSpl + ' - ';
        else:
            ArrToSpl = ArrToSpl + i;

    SplArr= ArrToSpl.split();
    return SplArr;

#Some code in this method is a copy from https://github.com/lilianweng/LeetcodePython/blob/master/expression.py
def InfxPosxConverter(formula):
    Pref = {'+': 1, '-': 1, '*': 2, '/': 2};
    Opts = set(['+', '-', '*', '/', '(', ')']);
    stk = [];
    Aux = "";
    for i in formula:
        if i not in Opts:
            Aux += i +" ";
        elif i == '(':
            stk.append('(');
        elif i == ')':
            while stk and stk[-1] != '(':
                Aux += stk.pop() + " ";
            stk.pop();
        else:
            while stk and stk[-1] != '(' and Pref[i] <= Pref[stk[-1]]:
                Aux += stk.pop() + " ";
            stk.append(i);

    while stk:Aux += stk.pop()+ " ";
    return Aux

#Some code in this method and the methos below is a copy from http://interactivepython.org/runestone/static/pythonds/BasicDS/InfixPrefixandPostfixExpressions.html

def Ev(PosExp):
    PosExpSpl = PosExp.split()
    OpStk = [];

    for i in PosExpSpl:
        if i.isdigit():
            OpStk.append(int(i))
        else:
            Op2 = OpStk.pop()
            Op1 = OpStk.pop()
            Res = doMath(i, Op1, Op2)
            OpStk.append(Res)
    return OpStk.pop()


def doMath(Opt, Op1, Op2):
    if(Opt == "/"):
        return Op1 // Op2
    elif(Opt == "*"):
        return Op1 * Op2
    elif(Opt == "+"):
        return Op1 + Op2;
    elif(Opt == "-"):
        return Op1 - Op2;

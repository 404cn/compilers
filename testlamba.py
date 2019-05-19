#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
from io import StringIO


_Result = StringIO('')
_Result.write("a")
_Result.write("b")
_Result.write("c")
_Result.write("d")
# in fact _Result.write("str" + "\n")

with open('./result.txt', 'at+') as f:
    f.write(_Result.getvalue())
    '''

'''
f = lambda x=2: x**2

print(f(3))
'''
'''

with open('./result.txt', 'at+') as f:
    if f.read() == '':
        f.write("void")
'''

'''
from functools import reduce

DIGITS = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}

def char2num(s):
    return DIGITS[s]

def str2int(s):
    return reduce(lambda x, y: x * 10 + y, map(char2num, s))


print(type(str2int("12345")))
'''
'''
with open('./result.txt', 'r') as f:
    while True:
        ch = f.read(1)
        if ch:
            print(ch)
            ch = f.read(1)
            while ch == '/':
                f.read(1)
                if ch == '/':
                    break
        else: break
            '''
'''
with open('./result.txt', 'r') as f:
    ch=f.read(1)
    while ch:
        while ch == '/' and f.read(1) == '*':
            f.read(1)
            
    print(i)
    '''
'''
from io import StringIO, BytesIO
with open('./example.txt', 'rb') as f:
        _EXAMPLE = BytesIO(f.read())
_EXAMPLE.seek(-1, 0)
print((_EXAMPLE.read(1)).decode('utf-8'))
'''


#输入文法求First集和Follow集
#要求大写字母表示非终结符，小写字母表示终结符
#最后一个产生式以$结尾或者输入$表示输入结束
#默认第一个产生式的→左边为起始符号
def inputGrammer():  #接收文法输入的函数
    grammer=[]#声明一个文法列表，用来保存该文法的各个产生式
    print('箭头请用符号→')
    print('空串请用符号ε')
    print('____________________________')
    while(True):
        production=input()
        if(production=='$'):
            break;
        elif (production[-1:] == '$'):  # 如果是最后一个产生式，把$去掉加入到文法中，并跳出循环
            grammer.append(production[:-1])
            break;
        else:
            grammer.append(production)
    return grammer
#print('____________________________')
def cut(grammer):#把包含选择运算符的产生式，分为两个，如把 F→(E)|id 分成 F→(E) 和 F→id ,这样之后会比较方便
    grammer1 = []
    for i in range(len(grammer)):
        s=grammer[i]
        if '|' in s:
            while True:
                index = s.find('|')
                grammer1.append(s[:index])
                index2 = s.find('→')
                s1=s[:index2 + 1] + s[index + 1:]
                if '|' not in s1:
                    grammer1.append(s1)
                    break
                else:
                    s=s1
        else:
            grammer1.append(grammer[i])
    return grammer1
#print('____________________________')
First={}#该文法的First集，以字典形式存储
Follow={}#该文法的Follow集，以字典形式存储
def initializeFirstAndFollow(grammer):#找到文法中的非终结符VN,并为其各自建立First集和Follow集
    VN=[]
    for i in range(len(grammer)):
        s=grammer[i]
        for j in range(len(s)):
            if(s[j]>='A' and s[j]<='Z'):
                if(j<len(s)-1 and s[j+1]=='\''):
                    vn=s[j]+'\''
                    if vn not in VN:
                        VN.append(vn)
                else:
                    vn = s[j] + ''
                    if vn not in VN:
                        VN.append(vn)
    global First
    global Follow
    for i in range(len(VN)):
        First[VN[i]]=[]
        Follow[VN[i]]=[]
    Follow[VN[0]].append('$')
# print('____________________________')
def findFirstVN(s):#找到字符串中的第一个非终结符
    length=len(s)
    for i in range(length):
        if s[i]>='A' and s[i]<='Z':
            if(i<length-1):
                if(s[i+1]=='\''):
                    return s[i:i+2]
                else:
                    return s[i]
            else:
                return s[i]
    return '$'#表示该字符串中没有非终结符
#print('____________________________')
def findNextVN(s):#找到字符串中的第二个非终结符
    #判断一下FirstVN的位置，与len(s)比较
    length=len(s)
    vn=findFirstVN(s)
    index=s.find(vn)
    length1=len(vn)
    return findFirstVN(s[index+length1:])
#print('____________________________')
def findLastVN(s):#找到字符串中的最后一个非终结符
    length=len(s)
    index=0
    if s[length-1:]<'A' or s[length-1:]>'Z':
        if s[length-1:]!='\'':
            return findFirstVN(s)
    for i in range(length):
        if s[i]>='A' and s[i]<='Z':
            index=i
    if index==length-1:
        return s[index]
    else:
        if s[index+1]=='\'':
            return s[index:index+2]
        else:
            return s[index]
#print('____________________________')
def lookVT(grammer):#扫描文法中的每一个产生式，如果产生式右边第一个符号是终结符，则把它加到产生式左边非终结符的First集中去
    global First
    for i in range(len(grammer)):
        s = grammer[i]
        index = s.find('→')
        left = s[:index]
        right= s[index + 1:]
        if right[0]<'A' or right[0]>'Z':
            if right[0]=='i' and 'id' not in First[left]:
                First[left].append('id')
            else:
                if right[0] not in First[left]:
                    First[left].append(right[0])
#print('____________________________')
def FFirst(grammer):
    '''
        扫描文法中的每一个产生式，对于产生式右边第一个符号不是非终结符的情况，
       把右边非终结符First集中的元素加入到左边非终结符的First集中去
      如果右边非终结符的First集中包含空串ε，则应找到该非终结符之后的一个非终结符
     把这个非终结符First集中的元素加入到左边非终结符的First集中去，此次类推
     '''
    for i in range(len(grammer)):
        s = grammer[i]
        index = s.find('→')
        right = s[index + 1:]
        if right[0]<'A' or right[0]>'Z':
            continue
        vn1 = findFirstVN(s)
        vn2 = findNextVN(s)
        flag=1
        while flag==1 and '$'!=vn2:
            for ss in First[vn2]:
                if ss not in First[vn1]:
                    First[vn1].append(ss)
            if 'ε' in First[vn2]:
                flag=1
                index=s.find(vn2)
                vn2=findLastVN(s[index:])
            else:
                flag=0
#print('____________________________')
def handleFirst(grammer):#求First集的函数
    lookVT(grammer)
    FFirst(grammer)
    FFirst(grammer)
#print('____________________________')
def scanVT(s):#扫描文法中的每一个产生式，如果箭头→右边有终结符的话，找到在它之前紧挨着它的一个非终结符，把该终结符加入到该非终结符的Follow集中去
    #print(s,"In scanVT")
    global Follow
    s1=s
    index=s1.find('→')
    s1=s1[index+1:]
    for i in range(len(s1)):
        if s1[i]<'A' or s1[i]>'Z':
            if s1[i]!='\'':
                if i>0 and s1[i-1]=='\'':
                    vn=s1[i-2:i]
                elif i>0:
                    vn=s1[i-1]
                else:
                    vn='$'
                if len(s1)==1 or s1=='id':
                    vn='$'
                if vn!='$':
                    if s1[i] =='i' or s1[i]=='d':
                        if 'id' not in Follow[vn]:
                            Follow[vn].append('id')
                    else:
                        if s1[i] not in Follow[vn]:
                            Follow[vn].append(s1[i])
    vn1=findFirstVN(s1)
    vn2=findNextVN(s1)#产生式右边只有两个非终结符？？
    if vn1!='$' and vn2!='$' and vn1+vn2 in s1:
        for si in First[vn2]:
            if si not in Follow[vn1] and si!='ε':
                Follow[vn1].append(si)
    #print("FOllOW")
    #print(Follow)
    #print("End of FOLLOW")

#print('____________________________')
def FFollow(grammer):
    '''
          扫描文法的每一个产生式，把第一个非终结符的Follow集去除空串ε加入到最后一个非终结符的Follow集中去
         如果最后一个非终结符的First集中有空串ε，
        则把第一个非终结符的Follow集去除空串ε加入到倒数第二个非终结符的FOllow集中去，依次类推
    '''
    for i in range(len(grammer)):
        s = grammer[i]
        vn1 = findFirstVN(s)
        vn2 = findLastVN(s)
        flag=1
        while flag==1 and vn1!=vn2:
            for ss in Follow[vn1]:
                if ss not in Follow[vn2]:
                    Follow[vn2].append(ss)
            if 'ε' in First[vn2]:
                flag=1
                index=s.find(vn2)
                vn2=findLastVN(s[:index])
            else:
                flag=0
#print('____________________________')
def handleFollow(grammer):#求Follow集的函数
    global Follow
    for i in range(len(grammer)):
        s=grammer[i]
        scanVT(s)
    FFollow(grammer)
#print('____________________________')
def showFirst():#显示First集
    global First
    for i in First.keys():
        print('First(',i,')= ',end="{ ")
        for j in First[i]:
            if j!=First[i][-1]:
                print(j,end=", ")
            else:
                print(j, end="")
        print("} ")
#print('____________________________')
def showFollow():#显示Follow集
    for i in Follow.keys():
        print('Follow(',i,')= ',end="{ ")
        for j in Follow[i]:
            if j!=Follow[i][-1]:
                print(j,end=", ")
            else:
                print(j,end="")
        print("} ")

#print('____________________________')
if __name__ == '__main__':
    print('____________________________')
    g=inputGrammer()#接收文法输入
    grammer=cut(g)#对产生式作处理
    initializeFirstAndFollow(grammer)#初始化First集和Follow集
    print('____________________________')
    handleFirst(grammer)#求First集
    showFirst()#显示First集
    print('____________________________')
    handleFollow(grammer)#求Follow集
    showFollow()#显示Follow集
    print('____________________________')
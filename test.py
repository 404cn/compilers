#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from io import StringIO

def getGrammer():
    # 声明一个文法列表，用来保存各个文法的产生式子
    grammer = []
    with open('./law.english.txt', 'r') as f:
        grammerFile = StringIO(f.read())
    while True:
        line = grammerFile.readline()
        if line:
            # 去掉末尾\n
            grammer.append(line[:-1])
        else:
            # 文件结束，跳出循环
            break
    return grammer
# 把包含选择运算符的产生式分为两个
def cutGrammer(grammer):
    j = 1
    grammerAfterCut = []
    for i in range(len(grammer)):
        line = grammer[i]
        if '|' in line:
            while True:
                print("line\t:\t%s"%line)
                index = line.find('|')
                print("index\t:\t%s"%index)
                print("line[:index]\t:\t%s"%line[:index])
                grammerAfterCut.append(line[:index])
                index1 = line.find('→')
                print("index1\t:\t%s"%index1)
                print("line[:index1 + 1]\t:\t%s"%line[:index1 + 1])
                print("line[index + 1:]\t:\t%s"%line[index + 1:])
                line1 = line[:index1 + 1] + line[index + 1:]
                print("line1\t:\t%s"%line1)
                print("j:%d\n\n"%j)
                j += 1
                if '|' not in line:
                    # TODO: 故意写错，只运行一次循环
                    grammerAfterCut.append[line1]
                    break
                else:
                    line = line1
        else:
            grammerAfterCut.append(grammer[i])
    return grammerAfterCut

# 文法的First集与Follow集，以字典形式存储
First = {}
Follow = {}
def main():
    grammer = getGrammer()
    print(cutGrammer(grammer))
main()
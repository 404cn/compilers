#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from io import StringIO

def grammer_from_file():
    # 声明一个文法列表，用来保存各个文法的产生式子
    grammer = []
    with open('./law.english.txt', 'r') as f:
        grammer_file = StringIO(f.read())
    while True:
        line = grammer_file.readline()
        if line:
            # 去掉末尾\n
            grammer.append(line[:-1])
        else:
            # 文件结束，跳出循环
            break
    return grammer
# 把包含选择运算符的产生式分为两个
def grammer_cut(grammer):
    grammer_after_cut = []
    for i in range(len(grammer)):
        line = grammer[i]
        if '|' in line:
            while True:
                index_of_or = line.find('|')
                grammer_after_cut.append(line[:index_of_or])
                index_of_derive = line.find('→')
                new_line = line[:index_of_derive + 1] + line[index_of_or + 1:]
                if '|' not in new_line:
                    grammer_after_cut.append(new_line)
                    break
                else:
                    line = new_line
        else:
            grammer_after_cut.append(grammer[i])
    return grammer_after_cut

# 文法的First集与Follow集，以字典形式存储
first = {}
follow = {}

# 找到文法中的非终结符vn并为其建立各自的first集和follow集
def init_first_and_follow(grammer_after_cut):
    vns = []
    global first
    global follow
    for i in range(len(grammer_after_cut)):
        line = grammer_after_cut[i].split('→')
        vn = line[0]
        if vn not in vns:
            vns.append(vn)
    for i in range(len(vns)):
        first[vns[i]] = []
        follow[vns[i]] = []
    follow[vns[0]].append('$')

def  

def main():
    grammer = grammer_from_file()
    grammer_after_cut = grammer_cut(grammer)
    print(init_first_and_follow(grammer_after_cut))
main()
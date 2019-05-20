#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from io import StringIO

"""
从文件中获得文法
"""
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
            break
    return grammer

"""
把包含选择运算符的产生式分为两个
"""
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
# 判断字符串是否是非终结符号
is_vn = lambda x: x.isupper() and len(x) > 1
# 判断字符串是否是终结符号
is_vt = lambda x: not is_vn(x)

"""
找到文法中的非终结符vn并为其建立各自的first集和follow集
"""
def init_first_and_follow(grammer_after_cut):
    vns = []
    global first, follow
    for i in range(len(grammer_after_cut)):
        line = grammer_after_cut[i].split('→')
        vn = line[0]
        if vn not in vns: 
            vns.append(vn)
    for i in range(len(vns)):
        first[vns[i]] = []
        follow[vns[i]] = []
    follow[vns[0]].append('$')

"""
扫描文法中每一个产生式，如果右边第一个符号是一个非终结符号，
就把它加到产生式左边非终结符号的First集中去
"""
def first_vt_to_first(grammer_after_cut):
    global first, is_vt
    for i in range(len(grammer_after_cut)):
        line = grammer_after_cut[i]
        index_of_derive = line.find('→')
        vn = line[:index_of_derive]
        first_word = line[index_of_derive + 1:].split(' ')[0]
        if is_vt(first_word) and first_word not in first[vn]:
            first[vn].append(first_word)
               
"""
找到字符串中第一个非终结字符，没找到反回False
"""
def first_vn_from_line(line):
    # 得到右侧第一个字符串
    words_of_right = line.split('→')[1].split(' ')
    length = len(words_of_right)
    for i in range(length):
        if is_vn(words_of_right[i]):
            return words_of_right[i]
        elif i == length - 1:
            return False
    
"""
找到字符串中第二个非终结字符，没找到返回False
"""
def second_vn_from_line(line):
    length = len(line)
    first_vn = first_vn_from_line(line)
    if first_vn:
        index_of_first_vn = line.find(first_vn)
        length_of_first_vn = len(vn)

        
    else:
        return False

"""
找到字符串中最后一个非终结字符
"""
def last_vn_from_line(line):
    pass


def main():
    '''
    grammer = grammer_from_file()
    grammer_after_cut = grammer_cut(grammer)
    init_first_and_follow(grammer_after_cut)
    first_vt_to_first(grammer_after_cut)
    '''
    print(first_vn_from_line("PROGRAM→program identifier ; PARTOFPROGRAM"))
main()
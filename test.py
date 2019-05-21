#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from io import StringIO

# 文法的First集与Follow集，以字典形式存储
first = {}
follow = {}
# 判断字符串是否是非终结符号
is_vn = lambda x: x.isupper() and len(x) > 1
# 判断字符串是否是终结符号
is_vt = lambda x: not is_vn(x)
# 计算列表中非终结字符的数量
count_vn = lambda list_of_right: len(list(filter(is_vn, list_of_right)))

"""
从文件中获得文法，成功则返回一个list，其中每个元素为一行产生式.
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
把包含选择运算符的产生式分为两个.
grammer: list, 文法列表，每个元素为文法的一行产生式.
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

"""
找到文法中的非终结符vn并为其建立各自的first集和follow集.
grammer_after_cut: list, 被消除选择运算符后的文法，每个元素为一个产生式.
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
找到字符串中第一个非终结字符，没找到反回False.
line: String, 文法中的一行产生式.
"""
def first_vn_from_line(line):
    if line.find('→') != -1:
        # 得到右侧第一个字符串
        list_of_right = line.split('→')[1].split(' ')
    else:
        list_of_right = line.split(' ')
    length = len(list_of_right)
    for i in range(length):
        if is_vn(list_of_right[i]):
            return list_of_right[i]
        elif i == length - 1:
            return False

"""
找到字符串中第二个非终结字符，没找到返回False.
line: String, 文法中的一行产生式.
"""
def second_vn_from_line(line):
    first_vn = first_vn_from_line(line)
    if first_vn:
        index_of_first_vn = line.find(first_vn)
        length_of_first_vn = len(first_vn)
        return first_vn_from_line(line[index_of_first_vn + length_of_first_vn:])
    else:
        return False

"""
找到字符串中最后一个非终结字符，没找到返回False.
line: String, 文法中的一行产生式.
"""
def last_vn_from_line(line):
    list_of_right = line.split('→')[1].split(' ')
    # list_of_right 必须是一个list
    count = count_vn(list_of_right)
    if count == 0: return False
    elif count == 1: return first_vn_from_line(line)
    elif count == 2: return second_vn_from_line(line)
    else:
        for i in range(len(list_of_right)):
            if is_vn(list_of_right[-i]):
                return list_of_right[-i]

"""
扫描文法中每一个产生式，如果右边第一个符号是一个非终结符号，
就把它加到产生式左边非终结符号的First集中去.
grammer_after_cut: list, 被消除选择运算符后的文法，每个元素为一个产生式.
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
扫描文法中的每一个产生式，对于产生式右边第一个符号不是非终结符的情况，
把右边非终结符First集中的元素加入到左边非终结符的First集中去,
如果右边非终结符的First集中包含空串ε，则应找到该非终结符之后的一个非终结符,
把这个非终结符First集中的元素加入到左边非终结符的First集中去，此次类推.
grammer_after_cut: list, 被消除选择运算符后的文法，每个元素为一个产生式.
"""
def first_not_vt(grammer_after_cut):
    global first
    for i in range(len(grammer_after_cut)):
        line = grammer_after_cut[i]
        line_cut = line.split('→')
        vn_of_left = line_cut[0]
        part_of_right = line_cut[1]
        list_of_right = part_of_right.split(' ')

        if is_vt(list_of_right[0]):
            continue
        
        print()
    '''
    for i in range(len(grammer_after_cut)):
        # 右侧第一个为终结符，已经添加到左侧非终结符中
        if is_vt(list_of_right[0]):
            continue
        first_vn = first_vn_from_line(grammer_after_cut[i])
        print(first_vn)
        for j in range(len(first[first_vn])):
            if first[first_vn][j] not in first[vn_of_left]:
                first[vn_of_left].append(first[first_vn][i])
            elif 'ε' in first[list_of_right[0]]:
                second_vn = second_vn_from_line(grammer_after_cut[i])
                if second_vn not in first[vn_of_left]:
                    first[vn_of_left].extend(first[second_vn])
                    '''

"""
构造first集.
grammer: list, 文法列表，每个元素为文法的一行产生式.
"""
def first_property(grammer_after_cut):
    first_vt_to_first(grammer_after_cut)
    first_not_vt(grammer_after_cut)
    first_not_vt(grammer_after_cut)

def main():
    grammer = grammer_from_file()
    grammer_after_cut = grammer_cut(grammer)
    init_first_and_follow(grammer_after_cut)
    first_vt_to_first(grammer_after_cut)
    first_not_vt(grammer_after_cut)
main()
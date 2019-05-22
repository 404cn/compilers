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
    for line in grammer:
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
            grammer_after_cut.append(line)
    return grammer_after_cut

"""
找到文法中的非终结符vn并为其建立各自的first集和follow集.
grammer_after_cut: list, 被消除选择运算符后的文法，每个元素为一个产生式.
"""
def init_first_and_follow(grammer_after_cut):
    vns = []
    global first, follow
    for line in grammer_after_cut:
        vn = line.split('→')[0]
        if vn not in vns:
            vns.append(vn)
    for key in vns:
        first[key] = []
        follow[key] = []
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
    for line in grammer_after_cut:
        index_of_derive = line.find('→')
        vn = line[:index_of_derive]
        first_word = line[index_of_derive + 1:].split(' ')[0]
        if is_vt(first_word) and first_word not in first[vn]:
            first[vn].append(first_word)

"""
将first_index中的除了空以外的所有符号加入到first(vn)中，失败则返回False
vn: String, 非终结符
first_index: list, 需要被加入到first(vn)的列表
"""
def list_to_first(vn, first_index):
    # TODO:
    print('\n')
    print(vn)
    print('\n')
    if is_vn(vn) and type(first_index) == list:
        for value in first_index:
            # 将右侧第一个非终结符的first集中除了空全加入到左侧非终结符的first集中
            if value not in first[vn] and 'ε' != value:
                first[vn].append(value)
    else:
        print("传入参数的类型错误.")
        return False

"""

vn: String, 非终结符
grammer_after_cut: list, 被消除选择运算符后的文法，每个元素为一个产生式.
"""
def vns_from_loop(vn, grammer_after_cut):
    vns = []
    if is_vn(vn):
        for line in grammer_after_cut:
            # 获得产生式左侧的非终结符
            vn_from_left = line.split('→')[0]
            # 如果产生式左侧的非终结符与传入函数的非终结符相等
            if vn == vn_from_left:
                vn_from_right = line.split('→')[1].split(' ')[0]
                if is_vn(vn_from_right):
                    vns.append(vn_from_right)
                else:
                    vns.append(vn)
                    break
            else:
                continue
            # TODO:
        print(vns)
        return vns
    else:
        print("传入参数的类型错误.")
        return False

"""
查询vn的产生式，若右侧第一个符号为终结符，返回vn，若右侧第一个符号
为非终结符，则用这个非终结符代替vn继续查找，以此类推
vn: String, 非终结符
grammer_after_cut: list, 被消除选择运算符后的文法，每个元素为一个产生式.
"""
def vt_from_loop(vn, grammer_after_cut):
    # TODO:
    vns = []
    if is_vn(vn):
        for line in grammer_after_cut:
            # 获得产生式左侧的非终结符
            vn_from_left = line.split('→')[0]
            # 如果产生式右侧的非终结符与传入函数的非终结符相等
            if vn == vn_from_left:
                vn_from_right = line.split('→')[1].split(' ')[0]
                if is_vn(vn_from_right):
                    vns.append(vt_from_right)
                else:
                    vns.append(vn)
                    break
            else:
                continue
            '''
            print(vt_from_right)
            if is_vt(vt_from_right):
                return vn
            vn = vt_from_right
            vt_from_loop(vn, grammer_after_cut)
            '''
        print(vns)
    else:
        print("传入参数的类型错误.")
        return False

"""
扫描文法中的每一个产生式，对于产生式右边第一个符号是非终结符的情况，
把右边非终结符first集中除了空串ε的元素加入到左边非终结符的first集中去,
如果右边非终结符的first集中包含空串ε，则应找到该非终结符之后的一个非终结符,
把这个非终结符first集中的元素加入到左边非终结符的first集中去，此次类推.
如果全都包含空串ε, 则把ε加入到左侧非终结符的first集中去.
grammer_after_cut: list, 被消除选择运算符后的文法，每个元素为一个产生式.
"""
def first_not_vt(grammer_after_cut):
    global first
    for line in grammer_after_cut:
        line_cut = line.split('→')
        vn = line_cut[0]
        part_of_right = line_cut[1]
        list_of_right = part_of_right.split(' ')

        # 跳过右侧第一个是终结符的，因为已经被函数处理过加入到first中
        if is_vt(list_of_right[0]):
            continue

        # 标识一个产生式右边如果是所有非终结符是否都包含空
        flag = False
        # 右边列表中下标为index的非终结符的first集，一个列表
        first_index = first[list_of_right[0]]
        # 获得右侧第一个字符是终结符的vn.
        vn = vt_from_loop(vn, grammer_after_cut)
        # 将右侧第一个非终结符first集中的非空元素全部加到左侧非终结符的first集中
        list_to_first(vn, first_index)

        if 'ε' in first_index:
            for index in range(1, len(list_of_right)):
                # 如果第一个非终结符后面的词为终结符，则将它加入左侧非终结符的first集中，
                # 结束这个产生式的循环，分析下个产生式
                if is_vt(list_of_right[index]):
                    first[vn].append(list_of_right[index])
                    break

                # 右边列表中下标为index的非终结符的first集，一个列表
                first_index = first[list_of_right[index]]
                vn = vt_from_loop(vn, grammer_after_cut)
                list_to_first(vn, first_index)
                
                # 如果产生式右边都是非终结符并其first集都包含空
                if index == len(list_of_right) - 1:
                    flag = True
                # 如果第二个字符为非终结符并包含空，则继续向后查找，否则结束循环
                if 'ε' in first_index:
                    continue
                else:
                    break
        # 产生式右边都是非终结符并first集都包含空，则将空加入到左侧非终结符的first集中
        if flag:
            first[vn].append('ε')

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
    vns_from_loop("FACTOR", grammer_after_cut)
    '''
    init_first_and_follow(grammer_after_cut)
    first_vt_to_first(grammer_after_cut)
    first_not_vt(grammer_after_cut)
    '''
main()
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


def vns_from_grammer(grammer_after_cut):
    """获得一个被分割后文法中的所有非终结符
    """
    vns = []
    for production in grammer_after_cut:  # 获取所有非终结符，用列表存储(vns)
        vn = production.split('→')[0]  # 每个产生式的头部都是非终结符
        if vn not in vns:  # 去除重复的非终结符
            vns.append(vn)
    return vns


"""
找到文法中的非终结符vn并为其建立各自的first集和follow集.
grammer_after_cut: list, 被消除选择运算符后的文法，每个元素为一个产生式.
"""
def init_first_and_follow(grammer_after_cut):
    global first, follow
    vns = vns_from_grammer(grammer_after_cut)
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


def list_to_first(vn, first_of_index):
    """将first_of_index中的除了空以外的所有符号加入到first(vn)中，失败则返回False

    vn: String, 非终结符
    first_of_index: list, 需要被加入到first(vn)的列表
    """
    if is_vn(vn) and type(first_of_index) == list:
        for value in first_of_index:
            # 将右侧第一个非终结符的first集中除了空全加入到左侧非终结符的first集中
            if value not in first[vn] and 'ε' != value:
                first[vn].append(value)
    else:
        return False


def vns_from_loop(vn, grammer_after_cut):
    """如果vn右侧第一个字符为非终结符，则以右侧的非终结符代替vn继续查找，直到
    找到右侧第一个字符为终结符的vn，加入到列表中

    例：A->B|C B->b C->c  将A与文法传入，成功则返回列表['B', 'C']
    成功则返回列表，失败返回False
    vn: String, 非终结符
    grammer_after_cut: list, 被消除选择运算符后的文法，每个元素为一个产生式.
    TODO: 待解决问题，非终结符只能在产生式第一个，待处理既有非终结符又有终结符的情况
            待考虑方案，如果终结符在前，先将vn加入vns，进行下一次循环，如果有非终结符
            则将非终结符加入vns，从vns中删除先前加入的vn，这样便从vns中排除了自身
            (需要用到标识非标识是否需要return并结束循环)
    """
    vns = []
    vns_finally = []
    # 标记一个非终结符的产生式没有非终结符
    flag = True
    if is_vn(vn):
        for line in grammer_after_cut:
            # 获得产生式左侧的非终结符
            vn_from_left = line.split('→')[0]
            # 如果产生式左侧的非终结符与传入函数的非终结符相等
            if vn == vn_from_left:
                # 获得右侧第一个字符
                vn_from_right = line.split('→')[1].split(' ')[0]
                # 如果右侧第一个字符为非终结符，将它加入到列表中，继续循环
                # 如果该终非结符的多个产生式右侧第一个非终结符一样，则只加入一次
                if is_vn(vn_from_right) and vn_from_right not in vns:
                    vns.append(vn_from_right)
                    flag = False
                # 如果右侧第一个字符为终结符，将传入函数的非终结符加入列表并返回列表
                # 函数结束，返回列表
                elif is_vt(vn_from_right) and flag and vn_from_right not in vns:
                    vns.append(vn)
                    return vns
            # 如果不想等则继续查找下一个产生式
            else:
                continue
    else:
        return False
    # 遍历列表中每一个非终结符号
    for vn_from_vns in vns:
        # 递归找到右侧为终结符的非终结符
        new_vns = vns_from_loop(vn_from_vns, grammer_after_cut)
        # 将其加入列表中
        vns_finally.extend(new_vns)
    return vns_finally


def first_not_vt(grammer_after_cut):
    """扫描文法中的每一个产生式，对于产生式右边第一个符号是非终结符的情况，
    把右边非终结符first集中除了空串ε的元素加入到左边非终结符的first集中去,
    如果右边非终结符的first集中包含空串ε，则应找到该非终结符之后的一个非终结符,
    把这个非终结符first集中的元素加入到左边非终结符的first集中去，此次类推.
    如果全都包含空串ε, 则把ε加入到左侧非终结符的first集中去.

    grammer_after_cut: list, 被消除选择运算符后的文法，每个元素为一个产生式.
    """
    global first
    vn_already_handle = []
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
        # 表示产生式右边当前非终结符的first集是否包含空，默认为不包含
        # 如果产生式右边都是非终结符并起first集都包含空，也设置为False
        flag_of_one = False

        # 先将产生式右侧第一个非终结符的first集加入到vn的first集中
        list_to_first(vn, first[list_of_right[0]])

        # 解决重复求vns问题，因为某些非终结符有多个右侧第一个字符为非终结符的产生式
        if vn not in vn_already_handle:
            # 找到右侧第一个字符为终结符的非终结符
            vns = vns_from_loop(vn, grammer_after_cut)
        vn_already_handle.append(vn)

        # 将所有非终结符的first集中除了空以外的元素加入到vn的first集中去
        for vn_from_vns in vns:
            list_to_first(vn, first[vn_from_vns])
            if 'ε' in first[vn_from_vns]:
                flag_of_one = True

        # 如果产生式右边当前非终结符的first集中包含空
        while flag_of_one:
            for index in range(1, len(list_of_right)):
                # 如果第一个非终结符后面的词为终结符，则将它加入左侧非终结符的first集中，
                # 结束这个产生式的循环，分析下个产生式
                if is_vt(list_of_right[index]):
                    first[vn].append(list_of_right[index])
                    flag_of_one = False
                    break

                for vn_from_vns in vns:
                    list_to_first(vn, first[vn_from_vns])
                    if 'ε' not in first[vn_from_vns]:
                        flag_of_one = False

                # 如果产生式右边都是非终结符并其first集都包含空
                if index == len(list_of_right) - 1:
                    flag = True
                    flag_of_one = False
        # 产生式右边都是非终结符并first集都包含空，则将空加入到左侧非终结符的first集中
        if flag:
            first[vn].append('ε')


def first_property(grammer):
    """构造first集.

    grammer: list, 文法列表，每个元素为文法的一行产生式.
    """
    grammer_after_cut = grammer_cut(grammer)
    init_first_and_follow(grammer_after_cut)
    first_vt_to_first(grammer_after_cut)
    first_not_vt(grammer_after_cut)


def head2vn_follow(head_of_production, vn)
    """将head_of_production的follow集中的元素全部加入vn的follow集中.
    
    会去除重复的，但是不会去除空，此函数用于产生式中vn后的vn中包含空或者
    vn在产生式中只出现一次并后面没有任何元素的情况
    """
    global follow
    for follow_of_head in follow[head_of_production]:
        if follow_of_head not in follow[vn]:
            follow[vn].append(follow_of_head)


def first2follow(value, vn):
    """将value的first集中除了空之外的加入到vn的follow集
    """
    global first
    global follow
    for value_of_first in first[value]:
        if value_of_first not in follow[vn] and value_of_first != 'ε':
            follow[vn].append(value_of_first)


def after_vn(vn, list_of_body):
    """将list_of_body中vn后面的元素加入列表返回

    如果一个产生式中只包含一次vn并且vn为产生式最后一个字符，返回False
    否则将它后面的元素加入列表中返回

    如果一个产生式含有vn多次，则将每个vn后的字符加入列表中返回
    """
    values_after_vn = []
    if list_of_body.count(vn) == 1:
        if vn == list_of_body[-1]:
            return False
        else:
            values_after_vn.append(list_of_body[list_of_body.index(vn) + 1])
    else:
        for i in range(len(list_of_body) - 1):
            if list_of_body[i] == vn and list_of_body[i + 1] not in values_after_vn:
                values_after_vn.append(list_of_body[i + 1])
    return values_after_vn
        




#TODO: grammer
def follow_property(grammer_after_cut):
    """
    构造follow集.
    grammer: list, 文法列表，每个元素为文法的一行产生式.
    """
    global follow
    vns = vns_from_grammer(grammer_after_cut)  # 用来存储所有非终结符
    for vn in vns: # 遍历所有非终结符
        for production in grammer_after_cut:  # 遍历每个产生式
            head_of_production = production.split('→')[0]  # 产生式头
            list_of_body = production.split('→')[1].split(' ')  # 产生式体列表

            if vn in list_of_body:  # 如果某个非终结符的产生式中有当前非终结符
                # 获得产生式中vn后面的字符，type:list，有多个vn也一样
                # 如果只有一个vn并且为产生式最后一个符号则会返回False
                values_after_vn = after_vn(vn, list_of_body)
                # 如果该产生式只有一个要查找的vn并且为产生式的最后一个符号
                if not values_after_vn:
                    # 将产生式头部非终结符的follow集全部加入vn的follow集中
                    head2vn_follow(head_of_production, vn)
                else:
                    for value in values_after_vn:
                        if is_vt(value) and value not in follow[vn]:
                            follow[vn].append(value)
                            continue
                        elif is_vn(value):
                            first2follow(value, vn)
                            if 'ε' in first[value]:

            else:
                continue


def main():
    grammer = grammer_from_file()
    grammer_after_cut = grammer_cut(grammer)
    """
    first_property(grammer)
    for key in first.keys():
        print(key)
        print(first[key])
    print(follow)
    """
    follow_property(grammer_after_cut)
main()

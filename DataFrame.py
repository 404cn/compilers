#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from io import StringIO
try:
    import pandas as pd
except ModuleNotFoundError:
    print("错误:没有安装pandas.")


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


def vns_from_file():
    grammer = grammer_from_file()
    grammer_after_cut = grammer_cut(grammer)
    return vns_from_grammer(grammer_after_cut)


def vts_from_grammer(grammer_after_cut):
    """获得一个被分割文法后的所有终结符
    """
    vts = []
    for production in grammer_after_cut: 
        list_of_body = production.split('→')[1].split(' ')
        for vt in list_of_body:
            if is_vt(vt) and vt not in vts:
                vts.append(vt)
    return vts
    

def vts_from_file():
    grammer = grammer_from_file()
    grammer_after_cut = grammer_cut(grammer)
    return vts_from_grammer(grammer_after_cut)


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


def first_property(grammer_after_cut):
    """构造first集.
    """
    init_first_and_follow(grammer_after_cut)
    first_vt_to_first(grammer_after_cut)
    first_not_vt(grammer_after_cut)


def head2vn_follow(head_of_production, vn):
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


def vt2follow(vt, vn):
    """将vt加入到vn的follow集中
    """
    global follow
    if vt not in follow[vn]:
        follow[vn].append(vt)


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
        

def one_vt_vn(grammer_after_cut):
    """产生式只有一次vn且vn后为vt，将vt加入vn的follow集中
    """
    global follow
    vns = vns_from_grammer(grammer_after_cut)
    for vn in vns:
        for production in grammer_after_cut:  # 遍历每个产生式
            list_of_body = production.split('→')[1].split(' ')  # 产生式体列表

            if list_of_body.count(vn) == 1 and vn != list_of_body[-1]:
                vt_after_vn = list_of_body[list_of_body.index(vn) + 1]
                if is_vt(vt_after_vn) and vt_after_vn not in follow[vn]:
                    follow[vn].append(vt_after_vn)


def one_last_vn(grammer_after_cut):
    """如果产生式只出现一个vn且vn为最后一个元素，则将产生式头部的follow集加入到vn
    的follow集中
    """
    global follow
    vns = vns_from_grammer(grammer_after_cut)
    for vn in vns:
        for production in grammer_after_cut:  # 遍历每个产生式
            head_of_production = production.split('→')[0]  # 产生式头
            list_of_body = production.split('→')[1].split(' ')  # 产生式体列表
            if list_of_body.count(vn) == 1 and vn == list_of_body[-1]: 
                head2vn_follow(head_of_production, vn)


# TODO: 待解决：如果value_after_vn后面的元素也在list中出现多次
# TODO: 则list.index(vt_after_value)会出现逻辑错误
# TODO: 如果出现多次，可以每次index后用一个确定不会出现在列表中的元素替换，
# TODO: 这样下一次index就不会出现重复的问题
def recursion_vn(value_after_vn, vn, head_of_production, list_of_body):
    """找到产生时list_of_body中value_after_vn的下一个元素，如果为vt则将其加入vn的
    follow集中，结束。
    如果为vn则将其first集加入vn的follow集，如果其first集包含空，则继续查找。
    如果后面都是vn且first集都包含空，则将head_of_production的follow集加入vn
    的follow集中
    """
    # TODO: 后续更改，更好的判断方法，其他部分代码也应该改，有时间再说：）
    if list_of_body.index(value_after_vn) == len(list_of_body) - 1:
        head2vn_follow(head_of_production, vn)
    else:
        vt_after_value = list_of_body[list_of_body.index(value_after_vn) + 1]
        while True:
            if is_vt(vt_after_value):
                if vt_after_value not in follow[vn]:
                    follow[vn].append(vt_after_value)
                break
            if is_vn(vt_after_value):
                first2follow(vt_after_value, vn)
                if 'ε' in first[vt_after_value]:
                    iterable_vn(vt_after_value, vn, head_of_production, list_of_body)


def one_vn_after_vn(grammer_after_cut):
    """处理产生时中只出现一次vn并且vn后面的字符为vn时的情况

    将后边的vn的first集中非空元素加入要查找的vn的follow集中，如果后边的
    vn包含空，则继续向后查找，直到找到vt或者要查找的vn后面全是非终结符并且
    都包含空，则把产生式头部非终结符的follow集加入要查找的vn的follow集中
    """
    global follow
    vns = vns_from_grammer(grammer_after_cut)
    for vn in vns:
        for production in grammer_after_cut:  # 遍历每个产生式
            head_of_production = production.split('→')[0]  # 产生式头
            list_of_body = production.split('→')[1].split(' ')  # 产生式体列表
            if list_of_body.count(vn) == 1 and vn != list_of_body[-1]:
                value_after_vn = list_of_body[list_of_body.index(vn) + 1]
                if is_vn(value_after_vn):
                    first2follow(value_after_vn, vn)
                    if 'ε' in first[value_after_vn]:
                        recursion_vn(value_after_vn, vn, head_of_production, list_of_body)


# TODO:虽然分产生式又一次vn与多次vn分开求后逻辑清晰一些，但是会多次便利产生式子
# TODO:带来效率上的下降，并且如ALPHABET与NUM会查几十次。。有待改善
# TODO:可以将for循环下代码写在一起并加continue解决(未测试)
def one_vn_follow(grammer_after_cut):
    """处理产生式中只出现一次vn的情况
    """
    one_vt_vn(grammer_after_cut)
    one_last_vn(grammer_after_cut)
    one_vn_after_vn(grammer_after_cut)


def vn_after_vn(value_after_vn, vn, head_of_production, list_of_body):
    """处理求vn的follow集的过程中vn后的元素是非终结符的情况
    """
    if value_after_vn == vn:
        return
    first2follow(value_after_vn, vn)
    if list_of_body[list_of_body.index(value_after_vn)] == len(list_of_body) - 1:
        head2vn_follow(head_of_production, vn)
    elif is_vt(value_after_vn):
        vt2follow(value_after_vn, vn)
    elif 'ε' in first[value_after_vn]:
        vt_after_value = list_of_body[list_of_body.index(value_after_vn) + 1]
        vn_after_vn(vt_after_value, vn, head_of_production, list_of_body)


def unone_vn_follow(grammer_after_cut):
    """处理产生式中不止有一次vn的情况
    """
    global follow
    vns = vns_from_grammer(grammer_after_cut)
    for vn in vns:
        for production in grammer_after_cut:  # 遍历每个产生式
            head_of_production = production.split('→')[0]  # 产生式头
            list_of_body = production.split('→')[1].split(' ')  # 产生式体列表

            if list_of_body.count(vn) > 1:
                for index in range(list_of_body.count(vn)):
                    index_of_vn = list_of_body.index(vn)
                    if index_of_vn != len(list_of_body) - 1:
                        value_after_vn = list_of_body[index_of_vn + 1]
                        if is_vt(value_after_vn):
                            follow[vn].append(value_after_vn)
                        else:
                            vn_after_vn(value_after_vn, vn, head_of_production, list_of_body)
                        list_of_body[index_of_vn] = None
                    else:
                        head2vn_follow(head_of_production, vn)
                    


def follow_property(grammer_after_cut):
    one_vn_follow(grammer_after_cut)
    unone_vn_follow(grammer_after_cut)
    # TODO: 待解决，求产生式中只有一次vn并且为最后一个元素是，产生式头的follow集还为空
    # TODO: 因为产生式头的follo集在求follow集时在产生式中出现多次，故还为空
    one_last_vn(grammer_after_cut)


def show_first():
    """格式化输出first集
    """
    global first
    for key in first.keys():
        print('First(', key, ')=', end='{')
        for value in first[key]:
            if value != first[key][-1]:
                print(value, end=',')
            else:
                print(value, end='')
        print('}')


def show_follow():
    """格式化输出follow集
    """
    global follow
    for key in follow.keys():
        print('Follow(', key, ')=', end='{')
        for value in follow[key]:
            if value != follow[key][-1]:
                print(value, end=',')
            else:
                print(value, end='')
        print('}')


def first_and_follow(grammer_after_cut):
    first_property(grammer_after_cut)
    follow_property(grammer_after_cut)


def init_data_frame(grammer_after_cut):
    vns = vns_from_grammer(grammer_after_cut)
    vts = vts_from_grammer(grammer_after_cut)
    dict_of_vts = {}
    for vt in vts:
        dict_of_vts[vt] = []
        for i in range(len(vns)):
            dict_of_vts[vt].append('')
    dict_of_vts['$'] = []
    for i in range(len(vns)):
        dict_of_vts['$'].append('')
    data_frame = pd.DataFrame(dict_of_vts, index=vns)
    return data_frame


def head_body_production(grammer_after_cut):
    """将产生式头与产生式体存储到字典中
    """
    dict_head_body = {}
    vns = vns_from_grammer(grammer_after_cut)
    for vn in vns:
        dict_head_body[vn] = []
    for production in grammer_after_cut: 
        head = production.split('→')[0]  
        body = production.split('→')[1]
        dict_head_body[head].append(body)
    return dict_head_body


'''
# TODO: error
def build_data_frame(grammer_after_cut, data_frame):
    """构建预测分析表
    """
    global first, follow
    vns = vns_from_grammer(grammer_after_cut)
    dict_head_body = head_body_production(grammer_after_cut)
    for vn in vns:
        for first_vn in first[vn]:
            data_frame.loc[vn][first_vn] = vn + '→' + dict_head_body[vn]
            if 'ε' in first[vn]:
                for follow_vn in follow[vn]:
                    data_frame.loc[vn][follow_vn] = vn + '→' + dict_head_body[vn]
                    if '$' in follow[vn]:
                        data_frame.loc[vn]['$'] = vn + '→' + dict_head_body[vn]
    return data_frame
    '''
def default_handle(data_frame, vn, first_vn, dict_head_body):
    """在构造预测分析表的过程中的默认处理方式
    """
    for value in dict_head_body[vn]:
        if len(dict_head_body[vn]) == 1:
            data_frame.loc[vn][first_vn] = vn + '→' + value
        elif len(dict_head_body[vn]) > 1:
            if first_vn == value:
                data_frame.loc[vn][first_vn] = vn + '→' + value

def none_in_first(data_frame, vn, dict_head_body):
    """处理在构造预测分析表的过程中vn的first集包含空的情况
    """
    global follow
    for follow_vn in follow[vn]:
        default_handle(data_frame, vn, follow_vn, dict_head_body)
        if '$' in follow[vn]:
            data_frame.loc[vn][follow_vn] = vn + '→' + dict_head_body[vn][0]

def build_data_frame(grammer_after_cut, data_frame):
    """构建预测分析表
    """
    global first
    vns = vns_from_grammer(grammer_after_cut)
    dict_head_body = head_body_production(grammer_after_cut)
    for vn in vns:
        for first_vn in first[vn]:
            default_handle(data_frame, vn, first_vn, dict_head_body)
            '''
            if 'ε' in first[vn]:
                none_in_first(data_frame, vn, dict_head_body)
                '''
    return data_frame


def data_frame():
    grammer = grammer_from_file()
    grammer_after_cut = grammer_cut(grammer)
    first_and_follow(grammer_after_cut)
    data_frame = init_data_frame(grammer_after_cut)
    # data_frame.loc['PROGRAM', 'program'] = ''
    return build_data_frame(grammer_after_cut, data_frame)
    

def productions():
    productions = []
    grammer = grammer_from_file()
    grammer_after_cut = grammer_cut(grammer)
    for production in grammer_after_cut:
        productions.append(production)
    return productions

"""
def main():
    # TODO: 一开始获得文法的时候就应该cut，有时间再改
    grammer = grammer_from_file()
    grammer_after_cut = grammer_cut(grammer)
    first_and_follow(grammer_after_cut)
    data_frame = init_data_frame(grammer_after_cut)
    # data_frame.loc['PROGRAM', 'program'] = ''
    build_data_frame(grammer_after_cut, data_frame)
main()
"""
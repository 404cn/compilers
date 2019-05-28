#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import DataFrame
from Stack import Stack

productions = DataFrame.productions()
data_map = DataFrame.data_frame()
vns = DataFrame.vns_from_file()
vts = DataFrame.vts_from_file()
stack = Stack()
tokens = []


def init_tokens():
    """用存储词法分析的结果的文件初始化tokens
    """
    global tokens
    with open("./result.txt", 'r') as f:
        buffer = f.read().split('\n')
        for i in range(len(buffer) - 1):
            if buffer[i].split(',')[1][1:-1] == '':
                tokens.append(',')
            else:
                tokens.append(buffer[i].split(',')[1][1:-1])
    tokens.append('$')


def next_token():
    """读取下一个token
    """
    global tokens
    token = tokens[0:1]
    tokens = tokens[1:]
    return str(token[0])


def init_stack():
    """初始化栈，将$(代表输入结束)与文法开始符压入栈中
    """
    global stack, vns
    stack.push('$')
    stack.push(vns[0])


def reverse_production_body_to_stack(production):
    """将产生式中每个元素逆向入栈
    """
    global stack
    reverse_body = production.split('→')[1].split(' ')
    reverse_body.reverse()
    for value in reverse_body:
        stack.push(value)


def parsing():
    global data_map, vns, vts, stack
    token = next_token()
    top = stack.peek()
    while top != '$':
        if top == token:
            print('匹配 ' + top)
            stack.pop()
            token = next_token()
        elif top == 'ε':
            stack.pop()
        elif DataFrame.is_vt(top):
            print('error, is_vt')
            print(stack)
            break
        elif data_map.loc[top][token] == '':
            print('error, 空')
            print(stack)
            break
        elif data_map.loc[top][token] in productions:
            print('输出 ' + data_map.loc[top][token])
            stack.pop()
            reverse_production_body_to_stack(data_map.loc[top][token])
        top = stack.peek()


def main():
    global data_map
    init_tokens()
    init_stack()
    parsing()
    '''
    data_map.to_csv('test.csv')
    DataFrame.show_first()
    DataFrame.show_follow()
    '''
main()

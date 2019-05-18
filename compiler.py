#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, os
from io import StringIO
from functools import reduce

# 将字符串转换为整形
DIGITS = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}
def char2num(s):
    return DIGITS[s]
def str2int(s):
    return reduce(lambda x, y: x * 10 + y, map(char2num, s))

"""
对file文件进行词法分析，将结果以格式化的形式写入
当前目录下的result.txt文件中.
"""
def scaner(file):
    with open(file, 'r') as f:
        _EXAMPLE = StringIO(f.read())
    # 每次从file中读取制定字节数
    getCharFromProgram = lambda x=1: _EXAMPLE.read(x)

    # 获取编码文件并序列化为字典
    with open('./scaner.json', 'r') as f:
        SCANER = json.loads(f.read())
    # result: 内存中用来存放结果的数据流
    _Result = StringIO('')

    # 如果文件不存在会自动创建
    Result = open('./result.txt', 'at+')
    # 如果文件不为空则删除文件内容
    if os.path.getsize('./result.txt') > 0:
        Result.seek(0)
        Result.truncate()

    while True:
        # token: 用来连接读取到的字符
        token = ''
        ch = getCharFromProgram()
        while ch in [' ', '\n', '\t']:
            continue
        # 判断是否到文件结束
        if ch:
            # 是否以字母开始或全是字母
            if ch.isalpha():
                token += ch
                ch = getCharFromProgram()
                # 是否全是字母或数字
                while ch.isalnum():
                    token += ch
                    ch = getCharFromProgram()
                # 将文件指针前移一位
                _EXAMPLE.seek(-1, 1)
                # 如果不在编码文件中，则为用户自定义标志符，否则为保留字
                if token not in SCANER:
                    _Result.write("(%d, %s)\n", 0, '')
                else:
                    _Result.write("(%d, %s)\n", SCANER[token], token)
            elif ch.isdigit():
                token += ch
                ch = getCharFromProgram()
                # TODO: 判断负数与小数
                while ch.isdigit():
                    token += ch
                    ch = getCharFromProgram()
                _EXAMPLE.seek(-1, 1)
                # 将字符串转换为二进制存储
                _Result.write("(%d, %s)\n", 1, int(str2int(token), base=2))
            elif ch in [',', ';', '+', '-', '*', '=', '.']:
                _Result.write("(%d, %s)\n", SCANER[ch], ch)
            elif ch in ['>', '<', ':']:
                token += ch
                ch = getCharFromProgram()
                if ch == '=':
                    token += ch
                    _Result.write("(%d, %s)\n", SCANER[token], token)
                else:
                    _EXAMPLE.seek(-1, 1)
                    _Result.write("(%d, %s)\n", SCANER[ch], ch)
            elif ch == '/':
                ch = getCharFromProgram()
                if ch == '/': _EXAMPLE.readline()
                elif ch == '*': # TODO: 判断多行注释
                else:
                    _EXAMPLE.seek(-1, 1)
                    _Result.write("(%d, %s)\n", SCANER[ch], ch)
            else: print("unknown symbol %s.", ch)
        else: break
    Result.writer(_Result.getvalue())
    Result.close()

def main():
    if (sys.argv[1]) and (len(sys.argv) == 2):
        scaner(sys.argv[1])
    else:
        print("请以正确格式运行。")

main()

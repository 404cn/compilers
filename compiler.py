#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
from io import StringIO

# 获取编码文件并序列化为字典
with open('./scaner.json', 'r') as f:
    SCANER = json.loads(f.read())
# 以文件形式操作内存中的字节流
with open('./Resault.txt', 'at+') as f:
    _Result = StringIO(f.read())

"""
param :
    file: 需要进行语法分析的文件
output : 以格式化的形式将结果写入Result文件中
"""
def scaner(file):
    with open(file, 'r') as f:
        EXAMPLE = StringIO(f.read())
    # 每次从file中读取制定字节数
    getCharFromProgram = lambda x:EXAMPLE.read(x)

    while True:
        ch = getCharFromProgram(1)
        while (ch == ' ') or (ch == '\n') or (ch == '\t'):
            ch = getCharFromProgram(1)
        # 判断是否到文件结束
        if ch:
            # 是否以字母开始或全是字母
            if ch.isalpha():
                # token: 用来连接读取到的字符
                token += ch
                ch = getCharFromProgram(1)
                i = 1
                # 是否全是字母或数字
                while ch.isalnum():
                    token += ch
                    i += 1
                    ch = getCharFromProgram(1)
                token[i] = '\0'
                # 将文件指针前移一位
                EXAMPLE.seek(-1, 1)
                # 如果不在编码文件中，则为用户自定义标志符，否则为保留字
                if token not in SCANER:
                    # TODO: out(o, token)
                else:
                    # TODO: out(SCANER[token], ' ')
            elif ch.isdigit():
            else: lambda ch: {
                }.get(ch, -1)(ch)
            
        else:
            break


if __name__ == "__main__":
    if (sys.argv[1]) and (len(sys.argv) == 2):
        scaner(sys.argv[1])
    else:
        print("请以正确格式运行。")

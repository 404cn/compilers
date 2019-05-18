#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, os
from io import StringIO, BytesIO
from functools import reduce

# 将字符串转换为整形
DIGITS = {
    '0': 0, '1': 1, '2': 2, '3': 3, '4': 4,
    '5': 5, '6': 6, '7': 7, '8': 8, '9': 9
    }
def char2num(s):
    return DIGITS[s]
def str2int(s):
    return reduce(lambda x, y: x * 10 + y, map(char2num, s))

# 获取编码文件并序列化为字典
with open('./complier.json', 'r') as f:
    SCANER = json.loads(f.read())

"""
构造一个格式化的字符串: (%d, %s)\n
"""
def buildFormatStr(token2code, token):
    return "(%d, %s)"%(SCANER[token2code], token)

"""
对file文件进行词法分析，将结果以格式化的形式写入
当前目录下的result.txt文件中.
"""
def scaner(file):
    # 字节流才能使用seek()改变文件指针pos
    with open(file, 'rb') as f:
        _EXAMPLE = BytesIO(f.read())
    # 每次从file中读取制定字节数
    getCharFromFile = lambda x=1: (_EXAMPLE.read(x)).decode('utf-8')

    # 如果文件不存在会自动创建
    Result = open('./result.txt', 'at+')
    # 如果文件不为空则删除文件内容
    if os.path.getsize('./result.txt') > 0:
        Result.seek(0)
        Result.truncate()

    # result: 内存中用来存放结果的数据流
    _Result = StringIO('')
    ch = getCharFromFile()
    while ch:
        print(ch)
        # token: 用来连接读取到的字符
        token = ''
        while ch in [' ', '\n', '\t']:
            ch = getCharFromFile()
        # 是否以字母开始或全是字母
        if ch.isalpha():
            token += ch
            ch = getCharFromFile()
            # 是否全是字母或数字
            while ch.isalpha() or ch in DIGITS:
                token += ch
                ch = getCharFromFile()
            # 如果不在编码文件中，则为用户自定义标志符，否则为保留字
            if token not in SCANER:
                _Result.write(buildFormatStr("ID", ''))
            else:
                _Result.write(buildFormatStr(token,token))
        elif ch in DIGITS:
            token += ch
            ch = getCharFromFile()
            # TODO: 判断负数与小数
            while ch in DIGITS:
                token += ch
                ch = getCharFromFile()
            # 将字符串转换为二进制存储，二进制以0b开头，故使用[2:]
            _Result.write(buildFormatStr("NUM", bin(int(token))[2:]))
        elif ch in [',', ';', '+', '-', '*', '=', '.']:
            _Result.write(buildFormatStr(ch, ch))
            ch = getCharFromFile()
        elif ch in ['>', '<', ':']:
            token += ch
            ch = getCharFromFile()
            if ch == '=':
                token += ch
                _Result.write(buildFormatStr(token, token))
                ch = getCharFromFile()
            else:
                _EXAMPLE.seek(-1, 1)
                _Result.write(buildFormatStr(ch, ch))
        elif ch == '/':
            ch = getCharFromFile()
            if ch == '/':
                _EXAMPLE.readline()
                ch = getCharFromFile()
            elif ch == '*': 
                while ch:
                    if getCharFromFile() == '*' and getCharFromFile() == '/':
                        ch = getCharFromFile()
                        break
            else:
                _EXAMPLE.seek(-1, 1)
                _Result.write(buildFormatStr(ch, ch))
        else: 
            print("unknown symbol %s"%ch)
            break
    Result.write(_Result.getvalue())
    Result.close()

def main():
    if (sys.argv[1]) and (len(sys.argv) == 2):
        scaner(sys.argv[1])
    else:
        print("请以正确格式运行。")

main()

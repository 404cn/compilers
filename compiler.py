#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, os
from io import StringIO, BytesIO

"""
对file文件进行词法分析，将结果以格式化的形式写入
当前目录下的result.txt文件中.
"""
def scaner(file):
    DIGITS = {
        '0': 0, '1': 1, '2': 2, '3': 3, '4': 4,
        '5': 5, '6': 6, '7': 7, '8': 8, '9': 9
        }
    # 获取编码文件并序列化为字典
    with open('./complier.json', 'r') as f:
        SCANER = json.loads(f.read())
    # 字节流才能使用seek()改变文件指针pos
    with open(file, 'rb') as f:
        _EXAMPLE = BytesIO(f.read())
    # 每次从file中读取制定字节数，如果文件不存在会自动创建
    Result = open('./result.txt', 'at+')
    # 如果文件不为空则删除文件内容
    if os.path.getsize('./result.txt') > 0:
        Result.seek(0)
        Result.truncate()
    # result: 内存中用来存放结果的数据流
    _Result = StringIO('')
    getCharFromFile = lambda size=1: (_EXAMPLE.read(size)).decode('utf-8')
    buildFormatStr = lambda key, token: "(%d, %s)\n"%(SCANER[key], token)

    ch = getCharFromFile()
    while ch:
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
                _Result.write(buildFormatStr("ID", token))
            else:
                _Result.write(buildFormatStr(token, ''))
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
            # 使用_ch代替ch进行判断，否则SCANER[ch]会发生KeyError:ch
            _ch = getCharFromFile()
            if _ch == '=':
                token += _ch
                _Result.write(buildFormatStr(token, token))
                ch = getCharFromFile()
            else:
                _EXAMPLE.seek(-1, 1)
                _Result.write(buildFormatStr(ch, ch))
                ch = getCharFromFile()
        elif ch == '/':
            _ch = getCharFromFile()
            if _ch == '/':
                _EXAMPLE.readline()
                ch = getCharFromFile()
            elif _ch == '*': 
                while _ch:
                    if getCharFromFile() == '*' and getCharFromFile() == '/':
                        ch = getCharFromFile()
                        break
            else:
                _EXAMPLE.seek(-1, 1)
                _Result.write(buildFormatStr(ch, ch))
                ch = getCharFromFile()
        else: 
            print("unknown symbol %s"%ch)
            break
    Result.write(_Result.getvalue())
    Result.close()

def main():
    if len(sys.argv) == 1: 
        file = input("请输入待分析文件路径：")
        scaner(file)
    elif (sys.argv[1]) and (len(sys.argv) == 2):
        scaner(sys.argv[1])
    else:
        print("文件路径错误.")
main()
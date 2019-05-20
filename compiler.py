#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, os
from io import StringIO, BytesIO

"""
对file文件进行词法分析，将结果以格式化的形式写入
当前目录下的result.txt文件中.
"""
def scaner(file):
    digits = {
        '0': 0, '1': 1, '2': 2, '3': 3, '4': 4,
        '5': 5, '6': 6, '7': 7, '8': 8, '9': 9
        }
    # 获取编码文件并序列化为字典
    with open('./complier.json', 'r') as f:
        code_file = json.loads(f.read())
    # 字节流才能使用seek()改变文件指针pos
    with open(file, 'rb') as f:
        program_file = BytesIO(f.read())
    # 每次从file中读取制定字节数，如果文件不存在会自动创建
    result_file = open('./result.txt', 'at+')
    # 如果文件不为空则删除文件内容
    if os.path.getsize('./result.txt') > 0:
        result_file.seek(0)
        result_file.truncate()
    # result: 内存中用来存放结果的数据流
    char2memory = StringIO('')
    char_from_file = lambda size=1: (program_file.read(size)).decode('utf-8')
    format_string = lambda key, token: "(%d, %s)\n"%(code_file[key], token)

    ch = char_from_file()
    while ch:
        # token: 用来连接读取到的字符
        token = ''
        while ch in [' ', '\n', '\t']:
            ch = char_from_file()
        # 是否以字母开始或全是字母
        if ch.isalpha():
            token += ch
            ch = char_from_file()
            # 是否全是字母或数字
            while ch.isalpha() or ch in digits:
                token += ch
                ch = char_from_file()
            # 如果不在编码文件中，则为用户自定义标志符，否则为保留字
            if token not in code_file:
                char2memory.write(format_string("ID", token))
            else:
                char2memory.write(format_string(token, ''))
        elif ch in digits:
            token += ch
            ch = char_from_file()
            # TODO: 判断负数与小数
            while ch in digits:
                token += ch
                ch = char_from_file()
            # 将字符串转换为二进制存储，二进制以0b开头，故使用[2:]
            char2memory.write(format_string("NUM", bin(int(token))[2:]))
        elif ch in [',', ';', '+', '-', '*', '=', '.']:
            char2memory.write(format_string(ch, ch))
            ch = char_from_file()
        elif ch in ['>', '<', ':']:
            token += ch
            # 使用_ch代替ch进行判断，否则code_file[ch]会发生KeyError:ch
            _ch = char_from_file()
            if _ch == '=':
                token += _ch
                char2memory.write(format_string(token, token))
                ch = char_from_file()
            else:
                program_file.seek(-1, 1)
                char2memory.write(format_string(ch, ch))
                ch = char_from_file()
        elif ch == '/':
            _ch = char_from_file()
            if _ch == '/':
                program_file.readline()
                ch = char_from_file()
            elif _ch == '*':
                while _ch:
                    if char_from_file() == '*' and char_from_file() == '/':
                        ch = char_from_file()
                        break
            else:
                program_file.seek(-1, 1)
                char2memory.write(format_string(ch, ch))
                ch = char_from_file()
        else:
            print("unknown symbol %s"%ch)
            break
    result_file.write(char2memory.getvalue())
    result_file.close()

def main():
    if len(sys.argv) == 1:
        file = input("请输入待分析文件路径：")
        scaner(file)
    elif (sys.argv[1]) and (len(sys.argv) == 2):
        scaner(sys.argv[1])
    else:
        print("文件路径错误.")
main()

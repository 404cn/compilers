#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
from io import StringIO


_Result = StringIO('')
_Result.write("a")
_Result.write("b")
_Result.write("c")
_Result.write("d")
# in fact _Result.write("str" + "\n")

with open('./result.txt', 'at+') as f:
    f.write(_Result.getvalue())
    '''

'''
f = lambda x=2: x**2

print(f(3))
'''
'''

with open('./result.txt', 'at+') as f:
    if f.read() == '':
        f.write("void")
'''

'''
from functools import reduce

DIGITS = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}

def char2num(s):
    return DIGITS[s]

def str2int(s):
    return reduce(lambda x, y: x * 10 + y, map(char2num, s))


print(type(str2int("12345")))
'''
'''
with open('./result.txt', 'r') as f:
    while True:
        ch = f.read(1)
        if ch:
            print(ch)
            ch = f.read(1)
            while ch == '/':
                f.read(1)
                if ch == '/':
                    break
        else: break
            '''
'''
with open('./result.txt', 'r') as f:
    ch=f.read(1)
    while ch:
        while ch == '/' and f.read(1) == '*':
            f.read(1)
            
    print(i)
    '''
'''
from io import StringIO, BytesIO
with open('./example.txt', 'rb') as f:
        _EXAMPLE = BytesIO(f.read())
_EXAMPLE.seek(-1, 0)
print((_EXAMPLE.read(1)).decode('utf-8'))
'''

b = "222"
print(bin(int(b)))
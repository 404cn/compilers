#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
from io import StringIO

with open('./scaner.json', 'r') as f:
    SCANER = json.loads(f.read())
with open('./Resault.txt', 'at+') as f:
    _Result = StringIO(f.read())

def scaner(file):
    with open(file, 'r') as f:
        EXAMPLE = StringIO(f.read())
    
    while True:
        ch = EXAMPLE.read(1)
        while (ch == ' ') or (ch == '\n') or (ch == '\t'):
            ch = EXAMPLE.read(1)
        if ch:
            if ch.isalpha():
                token[0] = ch
                ch = EXAMPLE.read(1)
                i = 1
                while ch.isalnum():
                    token[i] = ch
                    i = i + 1
                    ch = EXAMPLE.read(1)
                token[i] = '\0'
                EXAMPLE.seek(-1, 1)
                if token not in SCANER:
                    # TODO: out(o, token)
                else:
                    # TODO: out(SCANER[token], ' ')
            elif ch.isdigit():
            else: 
            
        else:
            break



if __name__ == "__main__":
    if (sys.argv[1]) and (len(sys.argv) == 2):
        scaner(sys.argv[1])
    else:
        print("请以正确格式运行。")

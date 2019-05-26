#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import DataFrame
from Stack import Stack

data_map = DataFrame.data_frame()
vns = DataFrame.vns_from_file()
vts = DataFrame.vts_from_file()
stack = Stack()
tokens = []


def init_tokens():
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
    global tokens
    token = tokens[0:1]
    tokens = tokens[1:]
    return str(token[0])


def main():
    init_tokens()
    print(next_token())
    print(next_token())
    print(next_token())
    print(next_token())
    print(next_token())
    print(next_token())
main()
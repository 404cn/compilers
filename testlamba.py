#!/usr/bin/env python3
# -*- coding: utf-8 -*-



def f(x):
    return {
            '>': print("this plan 0"),
            '<': print("this plan 1"),
            '=': print("this plan 2"),
        }.get(x)
f('>')


def num_to_string(num):
    numbers = {
        0 : print("zero"),
        1 : print("one"),
        2 : print("two"),
        3 : print("three")
    }
    return numbers.get(num, None)

print(num_to_string(0))

dict = {'Name': 'Zara', 'Age': 27}

print ("Value : %s" %  dict.get('Age'))
print ("Value : %s" %  dict.get('Sex', 'Age'))
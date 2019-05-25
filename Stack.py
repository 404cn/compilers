#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Stack(object):
    def __init__(self):
        self.stack = []

    def __bool__(self):
        return bool(self.stack)

    def __str__(self):
        return str(self.stack)

    def push(self, data):
        """ Push an element to the top of the stack."""
        self.stack.append(data)

    def pop(self):
        """ Pop an element off of the top of the stack."""
        if self.stack:
            return self.stack.pop()
        else:
            raise IndexError('pop from an empty stack')

    def peek(self):
        """ Peek at the top-most element of the stack."""
        if self.stack:
            return self.stack[-1]

    def is_empty(self):
        """ Check if a stack is empty."""
        return not bool(self.stack)

    def size(self):
        """ Return the size of the stack."""
        return len(self.stack)
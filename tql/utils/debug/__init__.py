#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
__title__ = '__init__.py'
__author__ = 'JieYuan'
__mtime__ = '2019-06-03'
"""

import pysnooper


@pysnooper.snoop()
def number_to_bits(number):
    if number:
        bits = []
        while number:
            number, remainder = divmod(number, 2)
            bits.insert(0, remainder)
        return bits
    else:
        return [0]

import numpy as np

@pysnooper.snoop()
def f():
    return np.arange(100000).shape

if __name__ == '__main__':
    f()
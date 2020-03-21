#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : hashcode
# @Time         : 2020-01-22 18:23
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : https://blog.csdn.net/R3eE9y2OeFcU40/article/details/82881685

# https://pypi.python.org/pypi/mmh3/2.3.1
# https://raw.githubusercontent.com/wc-duck/pymmh3/master/pymmh3.py
def convert_n_bytes(n, b):
    bits = b * 8
    return (n + 2 ** (bits - 1)) % 2 ** bits - 2 ** (bits - 1)


def getHashCode(s):
    h = 0
    n = len(s)
    for i, c in enumerate(s):
        h = h + ord(c) * 31 ** (n - 1 - i)
    return convert_n_bytes(h, 4)


##############
def getHashCode_(s):
    h = 0
    n = len(s)
    for i, c in enumerate(s):
        h += ord(c) * 31 ** (n - 1 - i)
    return (h + 2 ** 31) % 2 ** 32 - 2 ** 31


##############

import hashlib


def hashstr(s="12345", num_bins=1e4, suffix="suffix"):
    s += suffix
    return int(hashlib.md5(s.encode('utf-8')).hexdigest(), 16) % (num_bins - 1) + 1
    # return int(hashlib.md5(s.encode('utf-8')).hexdigest(), 16) % num_bins


import hashlib

def hash_fn(x, hashing_method='md5', N=2):
    tmp = [0 for _ in range(N)]
    for val in x:
        if val is not None:
            hasher = hashlib.new(hashing_method)
            hasher.update(bytes(str(val), 'utf-8'))
            tmp[int(hasher.hexdigest(), 16) % N] += 1
    return tmp

if __name__ == '__main__':
    print(hashstr("a"))

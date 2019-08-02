#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : subsets
# @Time         : 2019-07-25 22:40
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


def PowerSetsBinary(items, min_len=2, max_len=None):
    N = len(items)
    if max_len is None:
        max_len = N
    else:
        max_len = min(max_len, N)
    for i in range(2 ** N):  # 子集的个数
        combo = []
        for j in range(N):  # 用来判断二进制数的下标为j的位置的数是否为1
            if (i >> j) % 2:
                combo.append(items[j])
        if min_len <= len(combo) <= max_len:
            yield combo

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : pypytest
# @Time         : 2019-08-27 10:10
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

from tqdm import tqdm
import time


def test(n, m):
    m = m
    vals = []
    keys = []
    for i in tqdm(range(m)):
        vals.append(i)
        keys.append('a%s' % i)

    d = None
    for i in range(n):
        d = dict(zip(keys, vals))
    return d


if __name__ == '__main__':
    st = time.time()
    print(test(1000000, 100))
    print('use:', time.time() - st)
    print(f"{st}")

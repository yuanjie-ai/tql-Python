#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : numba
# @Time         : 2019-12-26 14:52
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


from numba import jit, njit, vectorize
import numpy as np

x = np.arange(100).reshape(10, 10)


# Numba likes NumPy broadcasting

# @jit
@njit  # 设置为"nopython"模式 有更好的性能
def go_fast1(a):  # 第一次调用时会编译
    trace = 0
    for i in range(a.shape[0]):  # Numba likes loops
        trace += np.tanh(a[i, i])  # Numba likes NumPy functions
    return a + trace



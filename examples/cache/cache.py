#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : cache
# @Time         : 2019-11-08 17:06
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

import time
from functools import lru_cache


@lru_cache(2)
def f(x):
    print("spleep 3s")
    time.sleep(3)
    return x


print(f(1))
print(f(1))
print(f._lru_cache_wrapper)



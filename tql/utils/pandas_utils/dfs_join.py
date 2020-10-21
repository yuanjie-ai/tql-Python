#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : dfs_join
# @Time         : 2020-02-13 20:26
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :
import pandas as pd
from functools import reduce


def dfs_join(dfs, key, map_fun=None):
    _ = reduce(lambda x, y: pd.merge(x, y, on=key), map(map_fun, dfs) if map_fun else dfs)
    return _



if __name__ == '__main__':
    df = pd.DataFrame([[1,2], [3,4]], columns=["a", "b"])

    print(dfs_join([df] * 3, "a"))


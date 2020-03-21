#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : expand
# @Time         : 2019-09-29 10:56
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

import pandas as pd

df = pd.DataFrame([['a', [1, 1], 'a b'],
                   ['b', [2, 2, 2], 'b c d'],
                   ['c', [3, 3, 3], 'c d e']],
                  columns=['id', 'feats', 's'])


class DataTrick(object):

    def __init__(self):
        pass

    def explode(self, df, col):
        df.explode(col)

    def expand(self, df, cols, sep=None):
        """

        :param df:
        :param cols: 列表 or 字符串
        :return: 变多列
        """
        df_ = df[:1]

        for col in cols:
            _type = df_[col].values[0]
            if isinstance(_type, (list, tuple)):
                _ = pd.DataFrame(df[col].tolist()).add_prefix(f'{col}_')
                df = pd.concat((df, _), 1)
            elif isinstance(_type, str):
                _ = df[col].str.split(sep, expand=True).add_prefix(f'{col}_')
                df = pd.concat((df, _), 1)
        return df

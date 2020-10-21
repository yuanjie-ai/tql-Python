#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : NumFeats
# @Time         : 2020/9/5 2:47 上午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :


import featuretools as ft
from .primitives import *

"""
可对topK特征暴力交叉
"""


# TODO 继承 AutoFeat

class NumFeats(object):

    def __init__(self, df: pd.DataFrame, index=None, max_depth=1, trans_primitives=None):
        self.df = df
        self.index = index
        self.max_depth = max_depth
        if trans_primitives is None:
            self.trans_primitives = [
                'divide_by_feature', 'absolute', 'percentile', 'add_numeric', 'subtract_numeric',
                'multiply_numeric', 'divide_numeric', PowerByFeature(0.5), PowerByFeature(2)
            ]

    def dfs(self, features_only=False):
        # 单表
        self.es = ft.EntitySet()
        self.es.entity_from_dataframe(
            entity_id='one',
            dataframe=df.copy(),
            index=self.index if self.index else '_id',
            make_index=self.index not in df.columns
        )
        _ = ft.dfs(entityset=self.es,
                   target_entity='one',
                   max_depth=self.max_depth,
                   verbose=1,
                   trans_primitives=self.trans_primitives,
                   features_only=features_only
                   )

        return _


if __name__ == '__main__':
    import pandas as pd

    df = pd.DataFrame({'a': range(5), 'b': range(1, 6)})

    print(NumFeats(df).dfs(False)[0])

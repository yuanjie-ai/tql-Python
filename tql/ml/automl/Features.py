#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : Features
# @Time         : 2019-07-26 10:04
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : featuretools

import featuretools as ft
from featuretools.selection import remove_low_information_features


class Features(object):
    """demo
    假如无时间列
    一拆多
    """

    def __init__(self, sparse_feats=None, dense_feats=None):
        self.sparse_feats = sparse_feats
        self.dense_feats = dense_feats
        self.es = ft.EntitySet(id='MAIN')

    def get_feats(self, df):
        self.es.entity_from_dataframe('df', df.copy(), index='ID')

        print("把类别当做ID拆成新表")
        # 这只是单key聚合
        for v in self.es['df'].variables:
            if v.dtype == 'categorical':
                self.es.normalize_entity('df', f'df_{v.name}', v.name)

        # todo: 多key聚合（如果不支持，先组合成单key）或者 获得 重要类别的子集组合
        # 多类别交叉得到更细的分组统计信息

        self.es.plot()
        df_feats, _ = ft.dfs(entityset=self.es, target_entity='df', verbose=1, max_depth=3, n_jobs=3)
        return df_feats

    def _subsets(self, items, min_len=2, max_len=None):
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

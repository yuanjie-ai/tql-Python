#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'rank_encoder'
__author__ = 'JieYuan'
__mtime__ = '19-3-11'
"""
from collections import OrderedDict

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class CountRankEncoder(BaseEstimator, TransformerMixin):

    def __init__(self, topn=None):
        """

        :param topn: 仅保留topn个类别
        """
        self.topn = topn
        self.mapper = None

    def fit(self, y):
        ce = pd.Series(y).value_counts(True, dropna=False)  # 计数编码
        if self.topn:
            ce = ce[:self.topn]
            print(f"Coverage: {ce.sum() * 100:.2f}%")

        self.mapper = ce.rank(method='first').to_dict(OrderedDict)  # rank 合理？
        return self

    def transform(self, y):
        """不在训练集的补0，不经常出现补0"""
        return pd.Series(y).map(self.mapper).fillna(0)


if __name__ == '__main__':
    import numpy as np

    s = ['a', 'a', 'b', 'b', 'c'] + [np.nan] * 6
    re = CountRankEncoder(2)

    print(re.fit_transform(s))
    print(re.mapper)

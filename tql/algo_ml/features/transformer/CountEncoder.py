#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'CountEncoder'
__author__ = 'JieYuan'
__mtime__ = '19-1-10'
"""
from collections import OrderedDict

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class CountEncoder(BaseEstimator, TransformerMixin):

    def __init__(self, dropna=False, normalize=False):
        """

        :param dropna: 缺失值是否计数，默认计数
        :param normalize: 频数还是频率，默认频数
        """
        self.dropna = dropna
        self.normalize = normalize
        self.mapper = None

    def fit(self, y):
        self.mapper = (pd.Series(y).value_counts(self.normalize, dropna=self.dropna)
                       .to_dict(OrderedDict))
        return self

    def transform(self, y):
        """不在训练集的补0，不经常出现补0"""
        return pd.Series(y).map(self.mapper).fillna(0)


if __name__ == '__main__':
    import numpy as np

    s = ['a', 'a', 'a', 'b', 'b'] + [np.nan] * 10
    ce = CountEncoder()
    print(ce.fit_transform(s))
    print(ce.mapper)

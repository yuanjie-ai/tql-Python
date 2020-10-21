#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : encoders
# @Time         : 2020/10/2 2:48 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

from collections import OrderedDict

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

from sklearn.preprocessing import LabelEncoder, OrdinalEncoder


class CountRankEncoder(object):

    def __init__(self, dropna=False):
        self.dropna = dropna

    def fit(self, y):
        self.mapper = (
            pd.Series(y).value_counts(dropna=self.dropna)
                .rank(method='first')
                .to_dict()
        )
        return self

    def transform(self, y):
        return pd.Series(y).map(self.mapper).fillna(0)


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
        self.mapper = (
            pd.Series(y).value_counts(self.normalize, dropna=self.dropna)
                .to_dict(OrderedDict)
        )
        return self

    def transform(self, y):
        """不在训练集的补0，不经常出现补0"""
        return pd.Series(y).map(self.mapper).fillna(0)


class RankEncoder(BaseEstimator, TransformerMixin):

    def __init__(self, na_option='keep', ascending=True):
        """
        na_option : {'keep', 'top', 'bottom'}, default 'keep'
            How to rank NaN values:

            * keep: assign NaN rank to NaN values
            * top: assign smallest rank to NaN values if ascending
            * bottom: assign highest rank to NaN values if ascending
        ascending : bool, default True
            Whether or not the elements should be ranked in ascending order.
        """
        self.na_option = na_option
        self.ascending = ascending

    def transform(self, y):
        return pd.Series(y).rank(method='first', na_option=self.na_option, ascending=self.ascending)


if __name__ == '__main__':
    import numpy as np

    s = ['a', 'a', 'a', 'b', 'b'] + [np.nan] * 10
    ce = CountEncoder()
    print(ce.fit_transform(s))
    print(ce.mapper)

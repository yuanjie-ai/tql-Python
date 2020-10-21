#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : RankEncoder
# @Time         : 2019-09-20 18:51
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 



import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class RankEncoder(BaseEstimator, TransformerMixin):

    def __init__(self, method='average', na_option='keep'):
        """
        method : {'average', 'min', 'max', 'first', 'dense'}, default 'average'
            How to rank the group of records that have the same value
            (i.e. ties):

            * average: average rank of the group
            * min: lowest rank in the group
            * max: highest rank in the group
            * first: ranks assigned in order they appear in the array
            * dense: like 'min', but rank always increases by 1 between groups
        numeric_only : bool, optional
            For DataFrame objects, rank only numeric columns if set to True.
        na_option : {'keep', 'top', 'bottom'}, default 'keep'
            How to rank NaN values:

            * keep: assign NaN rank to NaN values
            * top: assign smallest rank to NaN values if ascending
            * bottom: assign highest rank to NaN values if ascending
        ascending : bool, default True
            Whether or not the elements should be ranked in ascending order.
        """
        self.method = method
        self.na_option = na_option

    def transform(self, y):
        """不在训练集的补0，不经常出现补0"""
        return pd.Series(y).rank(method=self.method, na_option=self.na_option)  # .fillna(0)


if __name__ == '__main__':
    import numpy as np

    s = ['a', 'a', 'b', 'b', 'c'] + [np.nan] * 6
    re = RankEncoder(na_option='keep')


    print(re.transform(s))

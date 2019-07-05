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

    def __init__(self, normalize=False, dropna=False):
        self.dropna = dropna
        self.normalize = normalize
        self.mapper = None

    def fit(self, s: pd.Series):
        self.mapper = (s.value_counts(normalize=self.normalize, dropna=self.dropna)
                       .to_dict(OrderedDict))
        return self

    def transform(self, s: pd.Series):
        _ = s.map(self.mapper).fillna(0)  # 不在训练集的补0
        return _


if __name__ == '__main__':
    s = pd.Series(['a', 'a', 'a', 'b', 'b'])
    ce = CountEncoder()
    print(ce.fit_transform(s))
    print(ce.mapper)

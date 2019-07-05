#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
__title__ = 'DataAugment'
__author__ = 'JieYuan'
__mtime__ = '19-3-21'
"""

import pandas as pd
from sklearn.utils import shuffle


class DataAugment(object):

    def __init__(self, num_n, num_p, seed=0):
        """
        :param num_n: Negative sample enhancement multiple
        :param num_p: Positive sample enhancement multiple
        :param seed:
        """
        self.num_n = num_n
        self.num_p = num_p
        self.seed = seed

    def transform(self, X: pd.DataFrame, y):
        if not hasattr(y, 'tolist'):
            y = pd.Series(y)

        cols = X.columns
        X.columns = range(len(cols))
        Xn = self._augment(X[y == 0], self.num_n, self.seed)
        Xp = self._augment(X[y == 1], self.num_p, self.seed + 666666)

        X_ = pd.concat([X] + Xn + Xp, ignore_index=True)
        X_.columns = cols

        y_ = y.tolist() + [0] * (y == 0).sum() * self.num_n + [1] * y.sum() * self.num_p
        return X_, pd.Series(y_)

    def _augment(self, X, num, seed=0):
        return [X.apply(lambda x: shuffle(x.values, random_state=x.name + seed + i)) for i in range(num)]

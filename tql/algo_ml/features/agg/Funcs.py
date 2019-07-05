#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'functions'
__author__ = 'JieYuan'
__mtime__ = '19-1-15'
"""
import numpy as np


class Funcs(object):
    """x: pd.Series"""

    def __init__(self):
        self.num = ['q1', 'q3', 'iqr', 'kurt', 'cv', 'p2p']
        self.cat = ['mode', 'nunique_perc']

    @property
    def num_funcs(self):
        return [self.__getattribute__(func_name) for func_name in self.num]

    @property
    def cat_funcs(self):
        return [self.__getattribute__(func_name) for func_name in self.cat]

    # cat funcs
    def mode(self, x):
        return x.value_counts().index[0]

    def nunique_perc(self, x):
        return x.nunique() / x.count()

    # num funcs
    def q1(self, x):
        return x.quantile(0.25)

    def q3(self, x):
        return x.quantile(0.75)

    def iqr(self, x):
        return x.quantile(0.75) - x.quantile(0.25)

    def p2p(self, x):
        return np.ptp(x)

    def kurt(self, x):
        return x.kurt()

    def cv(self, x):
        return x.std() / (x.mean() + 1e-8)  # 变异系数

    def count_nonzero(self, x):
        return np.count_nonzero(x)

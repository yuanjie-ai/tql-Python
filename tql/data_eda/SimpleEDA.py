#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'SimpleEDA'
__author__ = 'JieYuan'
__mtime__ = '2019-04-22'
"""
import pandas as pd

from ..utils import cprint


class SimpleEDA(object):
    """
    1. 缺失值
    2. 方差/去重类别数/确定类别特征
    """

    def __init__(self, df: pd.DataFrame, exclude=None):
        self.df = df.drop(exclude, 1, errors='ignore') if exclude else df

        # self.df.head().T.add_prefix('row_')

    def summary(self, desc_rows=10):
        self._na(desc_rows)
        self._unique(desc_rows)

    def _na(self, desc_rows=10):
        cprint("\n1. 统计缺失率...")
        self.s_na = self.df.isnull().sum()[lambda x: x > 0].sort_values(0, False) \
                    / self.df.__len__() * 100
        print(self.s_na.head(desc_rows))

    def _unique(self, desc_rows=10):
        cprint("\n2. 统计类别数...")
        self.s_unique = self.df.nunique(dropna=False)[lambda x: x < 1024].sort_values()
        print(self.s_unique.head(desc_rows))

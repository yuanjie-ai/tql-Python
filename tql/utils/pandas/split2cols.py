#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'split2cols'
__author__ = 'JieYuan'
__mtime__ = '19-3-12'
"""
import pandas as pd

s = pd.Series([[1, 2, 3], [4, 5, 6]])

s.tolist()


def split2cols(series: pd.Series, columns=None):
    return pd.DataFrame(series.tolist(), columns=columns)

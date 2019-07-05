#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'row_feats'
__author__ = 'JieYuan'
__mtime__ = '19-2-25'
"""
from .Funcs import Funcs
import pandas as pd


class RowFeats(object):

    def __init__(self):
        pass

    def transform(self, df: pd.DataFrame, include=None, exclude=None):

        if not exclude is None and include is None:
            if exclude:
                df = df[exclude]
            else:
                df = df[[col for col in df.columns if col not in exclude]]
        else:
            df = df.copy()

        num_funcs = Funcs().num_funcs
        func_names = ['min', 'mean', 'median', 'max', 'sum', 'std', 'sem', 'skew', 'kurt']
        func_names_plus = ['q1', 'q3', 'iqr', 'kurt', 'cv', 'p2p']

        func = lambda x: [x.__getattr__(f)() for f in func_names] + [f(x) for f in num_funcs]
        df = df.apply(func, 1, result_type='expand')
        df.columns = func_names + func_names_plus
        return df

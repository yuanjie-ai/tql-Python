#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'AggFeat'
__author__ = 'JieYuan'
__mtime__ = '19-1-15'
"""
from .Funcs import Funcs
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor

import pandas as pd


class GroupFeats(object):

    def __init__(self, df, cat_cols, num_cols):
        self.df = df.copy()
        self.cat_cols = cat_cols
        self.num_cols = num_cols
        self.num_funcs = ['min', 'mean', 'median', 'max', 'sum', 'std', 'var', 'sem',
                          'skew'] + Funcs().num_funcs
        self.cat_funcs = ['nunique', 'max', 'min'] + Funcs().cat_funcs

    def transform(self, max_workers=4):
        with ProcessPoolExecutor(min(max_workers, len(self.cat_cols))) as pool:
            for _df in pool.map(self._get_agg_feats, tqdm(self.cat_cols, 'agg ...')):
                self.df = pd.merge(self.df, _df, 'left')
            return self.df

    def _get_agg_feats(self, key_cols):
        if isinstance(key_cols, str):
            key_cols = [key_cols]
        num_feats = self.num_cols
        cat_feats = list(set(self.cat_cols) - set(key_cols))

        gr = self.df.groupby(key_cols)
        trans_dict = dict(zip(num_feats + cat_feats + key_cols,
                              [self.num_funcs] * len(num_feats) \
                              + [self.cat_funcs] * len(cat_feats) \
                              + [['count']] * len(key_cols)))
        df = gr.agg(trans_dict)
        df.columns = ['&'.join(key_cols) + '_' + '_'.join(i) for i in df.columns]
        return df.reset_index()

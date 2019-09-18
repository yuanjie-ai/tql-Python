#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'VecFeats'
__author__ = 'JieYuan'
__mtime__ = '19-2-18'
"""
from sklearn.model_selection import cross_val_predict

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer


class VecFeats(object):

    def __init__(self, df, cat_feats, vectorizer=TfidfVectorizer(ngram_range=(1, 1), max_features=1000)):
        self.df = df
        self.cat_feats = cat_feats
        self.vectorizer = vectorizer

    def get_vectors(self):
        return self.vectorizer.fit_transform(self.corpus)

    @property
    def corpus(self):
        df = self.df[self.cat_feats]
        for idx, feat in enumerate(self.cat_feats):
            df[feat] = '%s_' % idx + df[feat].astype(str)
        return df.apply(lambda x: ' '.join(x), 1)

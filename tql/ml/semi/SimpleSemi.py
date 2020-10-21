#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'semi_simple'
__author__ = 'JieYuan'
__mtime__ = '19-1-11'
"""
import numpy as np
import pandas as pd
from tql.pipe import tqdm, cprint


class SimpleSemi(object):

    def __init__(self, clf, subsample=0.05, n_iter=1, scale_pos=1, mode=None, opt_seed=None):
        """

        :param subsample:
        :param n_iter:
        :param scale_pos: 正样本 / 负样本
        :param mode:
            'p': 从X_test, 只采样正样本
            'n': 从X_test, 只采样正样本
            None: 从X_test, 采样正+负样本
        """
        self.clf = clf
        self.subsample = subsample
        self.n_iter = n_iter
        self.scale_pos = scale_pos
        self.mode = mode
        self.opt_seed = opt_seed

        _ = "X_train will stack ≈ {:.2f}% of X_test".format(
            (1 - (1 - subsample - subsample * scale_pos) ** n_iter) * 100)
        cprint(_)

    def fit(self, X, y, X_test):
        self.X = X
        self.y = y
        self.X_test = np.asarray(X_test)

        for _ in tqdm(range(self.n_iter + 1)):
            self.clf.fit(self.X, self.y)
            _ = pd.Series(self.clf.predict_proba(self.X_test)[:, 1])

            if self.mode == 'n':
                pred = _.mask(lambda x: x < x.quantile(self.subsample), 0)
            elif self.mode == 'p':
                pred = _.mask(lambda x: x > x.quantile(1 - self.subsample * self.scale_pos), 1)
            else:
                pred = (_.mask(lambda x: x < x.quantile(self.subsample), 0)
                        .mask(lambda x: x > x.quantile(1 - self.subsample * self.scale_pos), 1))

            pred_ = pred[lambda x: x.isin([0, 1])]
            pseudo_label_idx = pred_.index
            no_pseudo_label_idx = pred.index.difference(pseudo_label_idx)

            self.X = np.row_stack((self.X, self.X_test[pseudo_label_idx]))
            self.y = np.hstack((self.y, pred_))

            self.X_test = self.X_test[no_pseudo_label_idx]
        return self.clf

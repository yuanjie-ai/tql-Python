#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'GaussRankScaler'
__author__ = 'JieYuan'
__mtime__ = '19-3-11'
"""

import scipy


class GaussRankScaler():
    """
    https://www.kaggle.com/mathormad/knowledge-distillation-with-nn-rankgauss
    https://blog.csdn.net/qq_33139511/article/details/79721590
    """

    def __init__(self):
        self.epsilon = 1e-9
        self.lower = -1 + self.epsilon
        self.upper = 1 - self.epsilon
        self.range = self.upper - self.lower

    def fit_transform(self, X):
        i = np.argsort(X, axis=0)
        j = np.argsort(i, axis=0)

        assert (j.min() == 0).all()
        assert (j.max() == len(j) - 1).all()

        j_range = len(j) - 1
        self.divider = j_range / self.range

        transformed = j / self.divider
        transformed = transformed - self.upper
        transformed = scipy.special.erfinv(transformed)
        ############
        # transformed = transformed - np.mean(transformed)

        return transformed

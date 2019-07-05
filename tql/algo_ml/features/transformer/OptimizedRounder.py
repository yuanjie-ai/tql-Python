#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'OptimizedRounder'
__author__ = 'JieYuan'
__mtime__ = '2019/4/4'
"""
import numpy as np
import pandas as pd
import scipy as sp

from functools import partial
from sklearn.metrics import cohen_kappa_score


# https://www.kaggle.com/naveenasaithambi/optimizedrounder-improved
class OptimizedRounder(object):
    def __init__(self):
        self.coef_ = 0

    def _kappa_loss(self, coef, X, y):
        preds = pd.cut(X, [-np.inf] + list(np.sort(coef)) + [np.inf], labels=[0, 1, 2, 3, 4])
        return -cohen_kappa_score(y, preds, weights='quadratic')

    def fit(self, X, y):
        loss_partial = partial(self._kappa_loss, X=X, y=y)
        initial_coef = np.percentile(X, [2.73, 23.3, 50.3, 72])  # <= improved
        self.coef_ = sp.optimize.minimize(loss_partial, initial_coef, method='nelder-mead')

    def predict(self, X, coef):
        preds = pd.cut(X, [-np.inf] + list(np.sort(coef)) + [np.inf], labels=[0, 1, 2, 3, 4])
        return preds

    def coefficients(self):
        return self.coef_['x']

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : OptimizedRounderF1
# @Time         : 2020/9/11 8:04 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


import numpy as np
import scipy as sp
import pandas as pd

from functools import partial
from sklearn import metrics


class OptimizedRounderF1(object):
    """
    An optimizer for rounding thresholds
    to maximize f1 score

    to maximize F1 (Macro) score
    # https://www.kaggle.com/naveenasaithambi/optimizedrounder-improved



    """

    def init(self):
        self.coef_ = 0

    def _f1_loss(self, coef, X, y):
        """
        Get loss according to
        using current coefficients

        :param coef: A list of coefficients that will be used for rounding
        :param X: The raw predictions
        :param y: The ground truth labels
        """
        X_p = pd.cut(X, [-np.inf] + list(np.sort(coef)) + [np.inf], labels=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

        return - metrics.f1_score(y, X_p)  # average='macro'

    def fit(self, y_pred, y_true):
        """
        Optimize rounding thresholds

        :param X: The raw predictions
        :param y: The ground truth labels
        """
        loss_partial = partial(self._f1_loss, X=y_pred, y=y_true)
        initial_coef = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5]
        self.coef_ = sp.optimize.minimize(loss_partial, initial_coef, method='nelder-mead')

    def predict(self, y_pred):
        """
        Make predictions with specified thresholds

        :param X: The raw predictions
        :param coef: A list of coefficients that will be used for rounding
        """
        coef = self.coef_['x']
        y_pred_round = pd.cut(y_pred, [-np.inf] + list(np.sort(coef)) + [np.inf],
                              labels=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

        return y_pred_round.astype(int)

    def coefficients(self):
        """
        Return the optimized coefficients
        """
        return self.coef_['x']

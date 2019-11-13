#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'semi_simple'
__author__ = 'JieYuan'
__mtime__ = '19-1-11'
"""
import numpy as np
import pandas as pd
from tqdm import tqdm


class SimpleSemi(object):

    def __init__(self, thresholds=(0.05, 0.995)):
        """
        :param thresholds: 分位数
        """
        self.thresholds = thresholds

    def get_X_y(self, preds, X, y, X_test):
        X_pseudo_0_index = np.where(preds < np.quantile(preds, self.thresholds[0]))[0]
        X_pseudo_1_index = np.where(preds > np.quantile(preds, self.thresholds[1]))[0]

        X_pseudo = np.r_[X_test[X_pseudo_0_index], X_test[X_pseudo_1_index]]
        y_pseudo = np.array([0] * len(X_pseudo_0_index) + [1] * len(X_pseudo_1_index))

        return np.r_[X, X_pseudo], np.r_[y, y_pseudo]

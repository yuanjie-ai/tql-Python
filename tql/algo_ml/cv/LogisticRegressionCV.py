#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : LogisticRegressionCV
# @Time         : 2019-09-17 22:33
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

import time
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.model_selection import StratifiedKFold, RepeatedStratifiedKFold
from sklearn.metrics import roc_auc_score
from scipy.sparse.csr import csr_matrix


class LogisticRegressionCV(object):

    def __init__(self, cv=5, random_state=None, n_repeats=None):
        self.clf = LogisticRegression(random_state=random_state, n_jobs=-1)

        if n_repeats:
            self._kf = RepeatedStratifiedKFold(cv, True, random_state)
            self._num_preds = cv * n_repeats
        else:
            self._kf = StratifiedKFold(cv, True, random_state)
            self._num_preds = cv

    def fit(self, X, y, X_test=None, feval=roc_auc_score, sample_weight=None):
        """输入数组"""
        if X_test is None:
            X_test = X[:1]

        self.oof_train = np.zeros(len(X) if not isinstance(X, csr_matrix) else X.shape[0])
        self.oof_test = np.zeros((len(X_test) if not isinstance(X, csr_matrix) else X_test.shape[0], self._num_preds))
        for n_fold, (train_index, valid_index) in enumerate(self._kf.split(X, y)):
            print("\033[94mFold %s started at %s\033[0m" % (n_fold + 1, time.ctime()))
            X_train, y_train = X[train_index], y[train_index]
            X_valid, y_valid = X[valid_index], y[valid_index]
            eval_set = [(X_train, y_train), (X_valid, y_valid)]

            ########################################################################
            self.clf.fit(X_train, y_train, sample_weight=None)

            self.oof_train[valid_index] = self.clf.predict_proba(X_valid)[:, 1]
            self.oof_test[:, n_fold] = self.clf.predict_proba(X_test)[:, 1]
            ########################################################################

        # 输出 测试集 oof
        self.oof_test_rank = (pd.DataFrame(self.oof_test).rank().mean(1) / len(self.oof_test)).values
        self.oof_test = self.oof_test.mean(1)

        # 计算 训练集 oof 得分
        if feval:
            self.oof_score = feval(y, self.oof_train)
            print(f"\n\033[94mCV Score: {self.oof_score} ended at {time.ctime()}\033[0m")
            return self.oof_score

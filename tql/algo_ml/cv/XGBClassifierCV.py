#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : BaseOOF
# @Time         : 2019-06-23 20:07
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :

import time
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold, RepeatedStratifiedKFold, KFold, cross_val_predict, cross_validate

from xgboost import XGBClassifier
from sklearn.metrics import roc_auc_score


class XGBClassifierCV(object):
    """cross_val_predict"""

    def __init__(self, params=None, cv=5, random_state=None, n_repeats=None):
        self.clf = XGBClassifier()
        if params:
            self.clf.set_params(**params)
        if n_repeats:
            self._kf = RepeatedStratifiedKFold(cv, True, random_state)
            self._num_preds = cv * n_repeats
        else:
            self._kf = StratifiedKFold(cv, True, random_state)
            self._num_preds = cv

    def fit(self, X, y, X_test=None, feval=roc_auc_score, sample_weight=None, eval_metric='auc',
            early_stopping_rounds=100, verbose=100, xgb_model=None, sample_weight_eval_set=None, callbacks=None):
        """输入数组"""
        if X_test is None:
            X_test = X[:1]

        self.oof_train = np.zeros(len(X))
        self.oof_test = np.zeros((len(X_test), self._num_preds))
        for n_fold, (train_index, valid_index) in enumerate(self._kf.split(X, y)):
            if verbose:
                print("\033[94mFold %s started at %s\033[0m" % (n_fold + 1, time.ctime()))
            X_train, y_train = X[train_index], y[train_index]
            X_valid, y_valid = X[valid_index], y[valid_index]
            eval_set = [(X_train, y_train), (X_valid, y_valid)]

            ########################################################################
            self.clf.fit(X_train, y_train, sample_weight, eval_set, eval_metric, early_stopping_rounds, verbose,
                         xgb_model, sample_weight_eval_set, callbacks)

            self.oof_train[valid_index] = self.clf.predict_proba(X_valid)[:, 1]
            self.oof_test[:, n_fold] = self.clf.predict_proba(X_test)[:, 1]
            ########################################################################

        # 输出 测试集 oof
        self.oof_test_rank = pd.DataFrame(self.oof_test).rank().mean(1) / len(self.oof_test)
        self.oof_test = self.oof_test.mean(1)

        # 计算 训练集 oof 得分
        if feval:
            score = feval(y, self.oof_train)
            print(f"\n\033[94mCV Score: {score} ended at {time.ctime()}\033[0m")
            return score

    def oof_save(self, file='./oof_train_and_test.csv'):
        assert isinstance(file, str)
        _ = np.append(self.oof_train, self.oof_test)
        pd.DataFrame(_, columns='oof_train_and_test').to_csv(file, index=False)


if __name__ == "__main__":
    from sklearn.datasets import make_classification

    X, y = make_classification()
    X_test, _ = make_classification()

    clf = XGBClassifierCV({'n_estimators': 1000})
    clf.fit(X, y, X_test)

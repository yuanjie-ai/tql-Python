#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : FMModelCV
# @Time         : 2019-10-15 16:38
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :


import time
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold, RepeatedStratifiedKFold, KFold, cross_val_predict, cross_validate
from sklearn.metrics import roc_auc_score

from xlearn import FMModel, FMModel


class FMModelCV(object):
    """cross_val_predict"""

    def __init__(self, params=None, cv=5, cv_seed=None, n_repeats=None):
        self.clf = FMModel()
        self.cv = cv
        if params:
            self.clf.set_params(**params)
        if n_repeats:
            self._kf = RepeatedStratifiedKFold(cv, True, cv_seed)
            self._num_preds = cv * n_repeats
        else:
            self._kf = StratifiedKFold(cv, True, cv_seed)
            self._num_preds = cv

    def fit(self, X, y, X_test=None, feval=roc_auc_score, fix_valid_index=None, fields=None,
            is_lock_free=True, is_instance_norm=True, is_quiet=False, verbose=1):

        if X_test is None:
            X_test = X[:1]

        self.oof_train = np.zeros(len(X))
        self.oof_test = np.zeros((len(X_test), self._num_preds))
        for n_fold, (train_index, valid_index) in enumerate(self._kf.split(X, y)):
            if verbose:
                print("\033[94mFold %s started at %s\033[0m" % (n_fold + 1, time.ctime()))

            # 设置valid早停范围
            if fix_valid_index is not None:
                valid_index = list(set(fix_valid_index) & set(valid_index))

            X_train, y_train = X[train_index], y[train_index]
            X_valid, y_valid = X[valid_index], y[valid_index]
            # eval_set = [(X_train, y_train), (X_valid, y_valid)]

            ########################################################################
            self.clf.fit(
                X_train,
                y_train,
                fields,
                is_lock_free,
                is_instance_norm,
                [X_valid, y_valid],
                is_quiet
            )
            self.oof_train[valid_index] = self.clf.predict(X_valid)
            self.oof_test[:, n_fold] = self.clf.predict(X_test)

            ########################################################################

        # 输出 测试集 oof
        self.oof_test_rank = (pd.DataFrame(self.oof_test).rank().mean(1) / len(self.oof_test)).values
        self.oof_test = self.oof_test.mean(1)

        assert len(X) == len(self.oof_train)
        assert len(X_test) == len(self.oof_test)

        # 计算 训练集 oof 得分
        if feval:
            self.oof_score = feval(y, self.oof_train)
            print("\n\033[94mScore Info:\033[0m")
            print(f"\033[94m     {self.cv:>2} CV: {self.oof_score:.6f}\033[0m")

            # _ = np.array(self.best_info['best_iteration'])
            # print(f"\033[94m      Iter: {_.mean():.0f} +/- {_.std():.0f}\033[0m")
            #
            # _ = np.array(self.best_info['best_score_valid'])
            # print(f"\033[94m     Valid: {_.mean():.6f} +/- {_.std():.6f} \033[0m\n")

        return self.oof_score

    @property
    def oof_train_and_test(self):
        return np.r_[self.oof_train, self.oof_test]


if __name__ == "__main__":
    from sklearn.datasets import make_classification

    X, y = make_classification(1000, random_state=666)

    clf = FMModelCV()
    clf.fit(X, y)

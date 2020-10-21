#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : base
# @Time         : 2020/9/5 7:12 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :

import time
import numpy as np
import pandas as pd
from abc import abstractmethod
from sklearn.model_selection import StratifiedKFold


class BaseOOF(object):

    def __init__(self, X, y, X_test=None, params=None, cv=5, feval=None, split_random_state=777):
        self.X = X
        self.y = y
        self.X_test = X_test if X_test is not None else self.X[:100]
        self.params = params
        self.feval = feval
        self.num_classes = len(set(self.y))

        self.oof_train_proba = np.zeros([len(X), self.num_classes])
        self.oof_test_proba_list = []

        # n_fold, (train_index, valid_index)
        self.n_fold2index = list(
            enumerate(StratifiedKFold(cv, shuffle=True, random_state=split_random_state).split(X, y)))

    @abstractmethod
    def fit_predict(self, X_train, y_train, X_valid, y_valid, X_test, **kwargs):
        """
        valid_predict, test_predict
        """
        raise NotImplementedError

    def run(self, oof_file=None):

        for n_fold, (train_index, valid_index) in self.n_fold2index:
            print(f"\033[94mFold {n_fold + 1} started at {time.ctime()}\033[0m")
            X_train, y_train = self.X[train_index], self.y[train_index]
            X_valid, y_valid = self.X[valid_index], self.y[valid_index]

            valid_predict, test_predict = self.fit_predict(X_train, y_train, X_valid, y_valid, self.X_test)

            self.oof_train_proba[valid_index] = valid_predict
            self.oof_test_proba_list.append(test_predict)

        self.oof_test_proba = np.mean(self.oof_test_proba_list, 0)  # num_classes

        if self.num_classes == 2:  # 二分类输出概率值
            self.oof_train = self.oof_train_proba[:, 1]
            self.oof_test = self.oof_test_proba[:, 1]
        else:  # 多分类输出类别值
            self.oof_train = np.argmax(self.oof_train_proba, 1)
            self.oof_test = np.argmax(self.oof_test_proba, 1)

        if self.feval is not None:
            self.oof_score = self.feval(self.y, self.oof_train)
            print(f"\033[94mCV Sorce: {self.oof_score} ended at {time.ctime()}\033[0m\n")

        if oof_file is not None:
            print("Save OOF Prediction")
            self.oof_train_test = np.r_[self.oof_train, self.oof_test]
            pd.DataFrame({'oof': self.oof_train_test}).to_csv(oof_file, index=False)

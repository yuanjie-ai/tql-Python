#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : KerasOOF
# @Time         : 2019-07-01 22:44
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :


import time
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold, KFold
from sklearn.metrics import roc_auc_score


class BaseEstimator(object):

    def fit(self, **kwargs):
        raise NotImplementedError

    def predict(self, X):
        """输出 n*1"""
        raise NotImplementedError


class CV(object):


    def __init__(self, estimator, cv=5, random_state=None):
        self._estimators = (estimator for _ in range(5))
        self.oof_train = None
        self.oof_test = None
        self._cv = cv
        self._kf = StratifiedKFold(cv, True, random_state)

    def _create_datas(self, X, y, X_test):
        self.oof_train = np.zeros(len(X))
        self.oof_test = np.zeros((len(X_test), self._cv))
        for (n_fold, (train_index, valid_index)), estimator in zip(enumerate(self._kf.split(X, y)), self._estimators):
            yield n_fold, estimator, train_index, valid_index

    def fit(self, X, y, X_test, feval=roc_auc_score):

        datas = self._create_datas(X, y, X_test)
        n_fold, estimator, train_index, valid_index = datas.__next__()
        print(f"\033[94mFold {n_fold + 1} started at {time.ctime()}\033[0m")
        X_train, y_train = X[train_index], y[train_index]
        X_valid, y_valid = X[valid_index], y[valid_index]

        ########################################################################
        # 二分类
        estimator.fit(X_train, y_train)
        self.oof_train[valid_index] = estimator.predict(X_valid)
        self.oof_test[:, n_fold] = estimator.predict(X_test)
        ########################################################################

        # 输出 测试集 oof
        self.oof_test_rank = pd.DataFrame(self.oof_test).rank().mean(1) / len(self.oof_test)
        self.oof_test = self.oof_test.mean(1)

        # 计算 训练集 oof 得分
        if feval:
            score = feval(y, self.oof_train)
            print(f"\n\033[94mCV Sorce: {score} ended at {time.ctime()}\033[0m")
            return score

#
# if __name__ == '__main__':
#     from tensorflow.python.keras.layers import Dense
#     from tensorflow.python.keras.models import Sequential
#
#
#     def create_model():
#         """from tensorflow.python.keras.models import clone_and_build_model"""
#         model = Sequential()
#         model.add(Dense(12, input_dim=20, kernel_initializer="uniform", activation="relu"))
#         model.add(Dense(8, kernel_initializer="uniform", activation="relu"))
#         model.add(Dense(1, kernel_initializer="uniform", activation="sigmoid"))
#         model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
#         return model
#
#
#     oof = KerasCV(create_estimator=create_model)
#     from sklearn.datasets import make_classification
#
#     X, y = make_classification(10000, shift=0.1)
#     oof.fit(X, y, X)

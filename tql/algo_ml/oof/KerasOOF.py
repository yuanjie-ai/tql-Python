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


class KearsOOF(object):
    """cross_val_predict"""

    def __init__(self, estimator_func, batch_size=128, epochs=10, callbacks=None, cv=5, random_state=None):
        self.estimators = [estimator_func() for _ in range(cv)]
        self.batch_size = batch_size
        self.epochs = epochs
        self.callbacks = callbacks
        self._kf = StratifiedKFold(cv, True, random_state)
        self._num_preds = cv

    def fit(self, X, y, X_test):
        """全数组
        :param X:
        :param y:
        :param X_test:
        :param feval:
        :return:
        """
        self.oof_train = np.zeros(len(X))
        self.oof_test = np.zeros((len(X_test), self._num_preds))
        for (n_fold, (train_index, valid_index)), estimator in zip(enumerate(self._kf.split(X, y)), self.estimators):
            print("\n\033[94mFold %s started at %s\033[0m" % (n_fold, time.ctime()))
            X_train, y_train = X[train_index], y[train_index]
            X_valid, y_valid = X[valid_index], y[valid_index]
            # eval_set = [(X_train, y_train), (X_valid, y_valid)]
            estimator.fit(X_train, y_train,
                          validation_data=(X_valid, y_valid),
                          batch_size=self.batch_size,
                          epochs=self.epochs,
                          callbacks=self.callbacks)

            ########################################################################
            # 二分类
            self.oof_train[valid_index] = estimator.predict(X_valid)[:, -1]  # num_sample * 1
            self.oof_test[:, n_fold] = estimator.predict(X_test)[:, -1]
            ########################################################################

        # 输出需要的结果
        self.oof_test_rank = pd.DataFrame(self.oof_test).rank().mean(1) / len(self.oof_test)
        self.oof_test = self.oof_test.mean(1)

    def oof_save(self, file=None):
        if file is None:
            file = self.estimators[0].__str__().split('(')[0][:32]
            file = '%s👍%s.csv' % (file, time.ctime())
        assert isinstance(file, str)
        _ = np.append(self.oof_train, self.oof_test)
        pd.DataFrame(_, columns='oof: train+test') \
            .to_csv(file, index=False)


if __name__ == '__main__':
    from tensorflow.python.keras.layers import Dense
    from tensorflow.python.keras.models import Sequential


    def create_model():
        """from tensorflow.python.keras.models import clone_and_build_model"""
        model = Sequential()
        model.add(Dense(12, input_dim=20, kernel_initializer="uniform", activation="relu"))
        model.add(Dense(8, kernel_initializer="uniform", activation="relu"))
        model.add(Dense(1, kernel_initializer="uniform", activation="sigmoid"))
        model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
        return model


    oof = KearsOOF(create_model)
    from sklearn.datasets import make_classification

    X, y = make_classification(10000, shift=0.1)
    oof.fit(X, y, X)

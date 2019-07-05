#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : demo
# @Time         : 2019-06-24 14:57
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :


import numpy as np
from sklearn.datasets import make_classification
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.wrappers.scikit_learn import KerasClassifier

from tql.algo_ml.oof import BaseOOF

import mlxtend.classifier.stacking_cv_classification
def create_model():
    model = Sequential()
    model.add(Dense(12, input_dim=20, kernel_initializer="uniform", activation="relu"))
    model.add(Dense(8, kernel_initializer="uniform", activation="relu"))
    model.add(Dense(1, kernel_initializer="uniform", activation="sigmoid"))
    model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])

    return model


X, y = make_classification(shift=0.1)
model = create_model()


class KerasModel(BaseOOF):
    def __init__(self, estimator, cv=5, epochs=5, callbacks=None):
        super().__init__(estimator, cv)
        self.epochs = epochs
        self.callbacks = callbacks

    def _fit(self, eval_set):
        _ = self.estimator.fit(*eval_set[0], validation_data=eval_set, callbacks=self.callbacks)
        return _


if __name__ == '__main__':
    KerasModel(estimator=model).fit(X, y, X)

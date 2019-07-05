#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : OOFlgb
# @Time         : 2019-06-23 23:41
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :
from lightgbm import LGBMClassifier

from .BaseOOF import BaseOOF


class LGB(BaseOOF):
    def __init__(self, estimator=LGBMClassifier(), cv=5, random_state=None, **kwargs):
        super().__init__(**kwargs)

    def _fit(self, eval_set):
        _ = self.estimator.fit(
            *eval_set[0],
            eval_set=eval_set,
            eval_metric="auc",
            early_stopping_rounds=100,
            verbose=100)
        return _


if __name__ == "__main__":
    from sklearn.datasets import make_classification

    X, y = make_classification()
    clf = LGB()
    clf.fit(X, y, X)

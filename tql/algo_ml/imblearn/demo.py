#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : demo
# @Time         : 2019-09-23 13:28
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


import time
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import KFold
from tql.algo_ml.cv import LGBMClassifierCV
import os
import socket

if socket.gethostname() == 'yuanjie-Mac.local':
    os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'


class UnderSamplerEnsemble(object):

    def __init__(self, params=None, cv=5, random_state=None):
        self.oof = LGBMClassifierCV(params, cv, random_state)

    def fit(self, X_p, X_n, X_test, cv=5, random_state=666, pred_ranking=False):
        kf = KFold(cv, True, random_state)

        self.preds = []
        for n_fold, (_, idx) in enumerate(kf.split(X_n)):
            print(f"UnderSamplerEnsemble {n_fold + 1} started at {time.ctime()}")
            X = np.r_[X_n[idx], X_p]
            y = np.r_[[0] * len(idx), [1] * len(X_p)]

            self.oof.fit(X, y, X_test)
            self.preds.append(self.oof.oof_test_rank if pred_ranking else self.oof.oof_test)

        return np.column_stack(self.preds).mean(1)


if __name__ == '__main__':
    from sklearn.metrics import roc_auc_score

    X, y = make_classification(
        n_classes=2, class_sep=1.5, weights=[0.999, 0.001],
        n_informative=3, n_redundant=1, flip_y=0,
        n_features=20, n_clusters_per_class=1,
        n_samples=10000, random_state=10
    )

    X_p = X[y == 1]
    X_n = X[y == 0]

    use = UnderSamplerEnsemble()
    preds = use.fit(X_p, X_n, X)
    print(roc_auc_score(y, preds))

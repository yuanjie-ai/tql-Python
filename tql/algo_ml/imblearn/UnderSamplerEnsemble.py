#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : UnderSamplerEmsemble
# @Time         : 2019-09-23 13:13
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :

import time
import numpy as np
from sklearn.model_selection import KFold
from ..cv import LGBMClassifierCV


class UnderSamplerEnsemble(object):

    def __init__(self, params=None, cv=5, random_state=None):
        self.oof = LGBMClassifierCV(params, cv, random_state)

    def fit(self, X_p, X_n, X_test, cv=5, random_state=666, pred_ranking=False):
        kf = KFold(cv, True, random_state)

        self.oof_preds = []
        self.oof_scores = []
        for n_fold, (_, idx) in enumerate(kf.split(X_n)):
            print(f"UnderSamplerEnsemble {n_fold + 1} started at {time.ctime()}")
            X = np.r_[X_n[idx], X_p]
            y = np.r_[[0] * len(idx), [1] * len(X_p)]

            _ = self.oof.fit(X, y, X_test)
            self.oof_scores.append(_)
            self.oof_preds.append(self.oof.oof_test_rank if pred_ranking else self.oof.oof_test)

        return np.row_stack(self.oof_preds)

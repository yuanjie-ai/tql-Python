#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'estimator_params_bounds'
__author__ = 'JieYuan'
__mtime__ = '19-3-19'
"""
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier as RFC


class ParamsBounds(object):
    """https://github.com/Jie-Yuan/optuna/blob/master/examples/lightgbm_simple.py"""


    @property
    def lgb(self):
        """https://www.cnblogs.com/wzdLY/p/9867719.html"""
        pass


    """https://github.com/fmfn/BayesianOptimization/blob/master/examples/sklearn_example.py"""
    @property
    def svc(self):
        estimator = SVC(random_state=123456)
        pbounds = {"C": (0.001, 100), "gamma": (0.0001, 0.1)}

        return estimator, pbounds

    @property
    def rfc(self):
        estimator = RFC(random_state=123456, n_jobs=-1)
        pbounds = {
            "criterion": ('gini', 'entropy'),
            "n_estimators": (32, 256),
            "min_samples_split": (2, 25),
            "max_features": (0.01, 1),
        }
        return estimator, pbounds



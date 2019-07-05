#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'estimator_params_bounds'
__author__ = 'JieYuan'
__mtime__ = '19-3-19'
"""
from lightgbm import LGBMClassifier, LGBMRegressor, LGBMRanker
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier as RFC


class ParamsBounds(object):
    """https://github.com/Jie-Yuan/optuna/blob/master/examples/lightgbm_simple.py"""

    def __init__(self):
        pass

    @property
    def lgb(self):
        """https://www.cnblogs.com/wzdLY/p/9867719.html"""
        # TODO: 其他 boosting_type

        estimator = LGBMClassifier(random_state=123456, subsample_freq=5)
        pbounds = {
            'learning_rate': (0.001, 0.1),
            'num_leaves': (2 ** 2, 2 ** 8),
            'min_split_gain': (0.01, 1),
            'min_child_weight': (0.001, 100),
            'min_child_samples': (16, 128),
            'subsample': (0.1, 1),
            'colsample_bytree': (0.01, 1),
            'reg_alpha': (0.01, 10),
            'reg_lambda': (0.01, 10)
        }
        return estimator, pbounds

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

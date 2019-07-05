#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'demo'
__author__ = 'JieYuan'
__mtime__ = '19-3-19'
"""
from lightgbm import LGBMClassifier
from sklearn.datasets import make_classification
from yuan.models.bayes_opt import Optimizer, ParamsBounds
from pprint import pprint

X, y = make_classification(
    n_samples=1000,
    n_features=45,
    n_informative=12,
    n_redundant=7,
    random_state=134985745,
)

estimator = LGBMClassifier(random_state=123456, subsample_freq=5, n_estimators=256)
pbounds = {
    'learning_rate': (0.001, 0.1),
    'num_leaves': (2 ** 2, 2 ** 8),
    'min_split_gain': (0.001, 1),
    'min_child_weight': (0.001, 10),
    'min_child_samples': (16, 128),
    'subsample': (0.6, 1),
    'colsample_bytree': (0.6, 1),
    'reg_alpha': (0.01, 10),
    'reg_lambda': (0.01, 10)
}

opt = Optimizer(estimator, pbounds)
pprint(opt.pbounds)
pprint(opt.scaled_pbounds)

opt.fit(X, y, 30)

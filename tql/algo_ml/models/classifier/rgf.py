#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'rgf'
__author__ = 'JieYuan'
__mtime__ = '19-1-2'
"""

from sklearn.model_selection import GridSearchCV
from rgf import RGFClassifier

rgf = RGFClassifier(
    max_leaf=1000,
    algorithm="RGF",
    loss="Log",
    l2=0.01,
    sl2=0.01,
    normalize=False,
    min_samples_leaf=10,
    n_iter=None,
    opt_interval=100,
    learning_rate=.5,
    calc_prob="sigmoid",
    n_jobs=8,
    memory_policy="generous"
)

parameters = {
    'max_leaf': [1000, 1200],
    'l2': [0.01, 0.1, 0.2, 0.3],
    'min_samples_leaf': [5, 10]
}

clf = GridSearchCV(
    estimator=rgf,
    param_grid=parameters,
    scoring='roc_auc',
    n_jobs=3,
    verbose=1,
    cv=3)

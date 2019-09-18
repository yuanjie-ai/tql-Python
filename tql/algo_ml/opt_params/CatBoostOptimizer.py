#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : XGBOptimizer
# @Time         : 2019-09-16 11:58
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 
import numpy as np
from .Optimizer import Optimizer
from catboost import CatBoostClassifier
from sklearn.model_selection import cross_val_score


class CatBoostOptimizer(Optimizer):

    def __init__(self, X, y, cv=5, workers=5, random_state=None, params_bounds=None):
        super().__init__(X, y, cv, workers, random_state, params_bounds)
        self.params_bounds = params_bounds if params_bounds else \
            dict(n_estimators=100,
                 loss_function="Logloss",
                 eval_metric="AUC",
                 task_type="GPU",
                 learning_rate=(0.001, 1),
                 l2_leaf_reg=(0, 100),
                 random_seed=666,
                 od_type="Iter",
                 depth=(2, 16),
                 early_stopping_rounds=300,
                 border_count=64,
                 has_time=True)

    def objective(self, **params):
        """重写目标函数"""

        # 纠正参数类型
        for p in ('max_depth', 'depth', 'num_leaves', 'subsample_freq', 'min_child_samples'):
            if p in params:
                params[p] = int(np.round(params[p]))
        _params = {**self.params_bounds, **params}

        # 核心逻辑
        self.clf = CatBoostClassifier(**_params)
        _ = cross_val_score(self.clf, self.X, self.y, scoring='roc_auc', cv=5, n_jobs=5).mean()
        return _

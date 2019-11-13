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
import catboost
from catboost import CatBoostClassifier
from sklearn.model_selection import cross_val_score, StratifiedKFold

from .Optimizer import Optimizer


class CatBoostOptimizer(Optimizer):

    def __init__(self, X, y, cv=5, cv_seed=None, params_bounds=None, use_gpu=1):
        super().__init__(X, y, cv, cv_seed, params_bounds)
        self.params_bounds = params_bounds if params_bounds else \
            dict(n_estimators=1000,
                 loss_function="Logloss",
                 eval_metric="AUC",
                 learning_rate=(0.001, 1),
                 l2_leaf_reg=(0, 100),
                 random_seed=666,
                 od_type="Iter",
                 depth=(2, 16),
                 early_stopping_rounds=300,
                 verbose=False,
                 border_count=64,
                 has_time=True)
        if use_gpu:
            self.workers = 1  # gpu 交叉验证只能单进程
            self.params_bounds.update({'task_type': 'GPU'})

    def objective(self, **params):
        """重写目标函数"""

        # 纠正参数类型
        params = self._round_params(params)
        _params = {**self.params_bounds, **params}

        # 核心逻辑 # TODO: 原生CV
        self.clf = CatBoostClassifier(**_params)
        scores = cross_val_score(self.clf, self.X, self.y, scoring='roc_auc',
                                 cv=StratifiedKFold(self.cv, True, self.cv_seed))
        return scores.mean()

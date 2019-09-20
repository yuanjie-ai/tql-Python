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
from xgboost import XGBClassifier
from sklearn.model_selection import cross_val_score

from .Optimizer import Optimizer


class XGBOptimizer(Optimizer):

    def __init__(self, X, y, cv=5, workers=5, random_state=None, params_bounds=None):
        super().__init__(X, y, cv, workers, random_state, params_bounds)

        self.params_bounds = params_bounds if params_bounds else \
            dict(n_estimators=100,
                 max_depth=(5, 16),
                 learning_rate=(0.001, 1),
                 max_delta_step=(0, 2), # 极端不平衡的时候有用

                 gamma=(0.001, 1),  # 描述分裂的最小 gain, 控制树的有用的分裂
                 min_child_weight=(0.001, 100),  # 决定最小叶子节点样本权重和,使一个结点分裂的最小权值之和, 避免过拟合

                 subsample=(0.1, 1),
                 colsample_bytree=(0.1, 1),  # 每棵树的列数
                 # colsample_bylevel=(0.3, 1),  # 每一层的列数

                 reg_alpha=(0, 6),
                 reg_lambda=(0, 6),

                 scale_pos_weight=1,

                 random_state=666,
                 n_jobs=-1,
                 verbosity=-1)

    def objective(self, **params):
        """重写目标函数"""

        # 纠正参数类型
        for p in ('max_depth', 'depth', 'num_leaves', 'subsample_freq', 'min_child_samples'):
            if p in params:
                params[p] = int(np.round(params[p]))
        _params = {**self.params_bounds, **params}

        # 核心逻辑
        self.clf = XGBClassifier(**_params)
        _ = cross_val_score(self.clf, self.X, self.y, scoring='roc_auc', cv=self.cv, n_jobs=self.workers).mean()
        return _

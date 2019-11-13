#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'Optimizer'
__author__ = 'JieYuan'
__mtime__ = '19-3-18'
"""

import json
import yaml
import numpy as np
import lightgbm as lgb
from tql.algo_ml.cv import LGBMClassifierCV, XGBClassifierCV

from .Optimizer import Optimizer


class LGBMOptimizer(Optimizer):
    """https://www.jianshu.com/p/1100e333fcab"""

    def __init__(self, X, y, cv=5, cv_seed=None, params_bounds=None):
        super().__init__(X, y, cv, cv_seed, params_bounds)
        self.best_iterations = []
        self.data = lgb.Dataset(X, y, silent=True, free_raw_data=True)

        self.params_bounds = params_bounds if params_bounds else \
            dict(  # cat_smooth
                metric='auc',
                class_weight=None,  # 'balanced'
                boosting_type='gbdt',
                num_leaves=(2 ** 2, 2 ** 7),
                learning_rate=(0.001, 1),
                min_split_gain=(0.001, 1),
                min_child_weight=(0.001, 64),  # 终点节点最小样本占比的和 TODO 确定范围
                min_child_samples=(16, 128),
                subsample=(0.1, 1),
                colsample_bytree=(0.1, 1),
                subsample_freq=(2, 6),
                reg_alpha=(0, 10),
                reg_lambda=(0, 10),
                n_jobs=-1,
                verbosity=-1,

                random_state=666,
                bagging_seed=0,
                feature_fraction_seed=0
            )

    def objective(self, **params):
        """重写目标函数"""

        # 纠正参数类型
        params = self._round_params(params)
        _params = {**self.params_bounds, **params}

        # 核心逻辑
        oof = LGBMClassifierCV(_params, self.cv, self.cv_seed)
        score = oof.fit(self.X, self.y, early_stopping_rounds=300, verbose=0)
        return score

    # def objective(self, **params):
    #     """重写目标函数"""
    #
    #     # 纠正参数类型
    #     params = self._round_params(params)
    #     _params = {**self.params_bounds, **params}
    #
    #     # 核心逻辑
    #     rst = lgb.cv(_params,
    #                  self.data,
    #                  num_boost_round=10000,
    #                  nfold=self.cv,
    #                  early_stopping_rounds=300,
    #                  verbose_eval=None,
    #                  show_stdv=False,
    #                  stratified=True,
    #                  shuffle=True,
    #                  seed=self.cv_seed)
    #
    #     scores = rst['auc-mean']
    #     self.best_iterations.append(len(scores))
    #     return scores[-1]

    @property
    def res(self):
        res = self.optimizer.res.copy()
        for res_, iteration in zip(res, self.best_iterations):
            _ = {**self.params_bounds, **res_['params'], 'n_estimators': iteration}
            res_['params'] = self._round_params(_)
        return res

    @property
    def best_params(self):
        return self.res[self.optimizer._space.target.argmax()]

    def to_file(self, file='opt', mode='json'):
        with open(f"{file}.{mode}", 'w') as f:
            if mode == 'json':
                json.dump(self.res, f, indent=4)
            else:
                yaml.safe_dump(eval(str(self.res)), f)

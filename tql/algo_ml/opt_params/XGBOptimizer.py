#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : XGBOptimizer
# @Time         : 2019-09-16 11:58
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

import json
import yaml
import numpy as np
import xgboost as xgb
from tql.algo_ml.cv import LGBMClassifierCV, XGBClassifierCV

from .Optimizer import Optimizer


class XGBOptimizer(Optimizer):

    def __init__(self, X, y, cv=5, cv_seed=0, params_bounds=None, use_gpu=1):
        super().__init__(X, y, cv, cv_seed, params_bounds)

        self.best_iterations = []
        self.data = xgb.DMatrix(X, y, silent=False, nthread=8)
        self.params_bounds = params_bounds if params_bounds else \
            dict(
                eval_metric='auc',
                booster='gbtree',
                objective='binary:logistic',

                max_depth=(3, 16),
                learning_rate=(0.001, 1),
                max_delta_step=(0, 2),  # 极端不平衡的时候有用

                gamma=(0.001, 1),  # 描述分裂的最小 gain, 控制树的有用的分裂
                min_child_weight=(0.001, 100),  # 决定最小叶子节点样本权重和,使一个结点分裂的最小权值之和, 避免过拟合

                subsample=(0.1, 1),
                colsample_bytree=(0.1, 1),  # 每棵树的列数
                # colsample_bylevel=(0.3, 1),  # 每一层的列数

                reg_alpha=(0, 10),
                reg_lambda=(0, 10),

                scale_pos_weight=1,

                random_state=666,
                n_jobs=-1,
                verbosity=0)

        if use_gpu:
            self.params_bounds.update({'tree_method': 'gpu_hist', 'predictor': 'gpu_predictor'})

    def objective(self, **params):
        """重写目标函数"""

        # 纠正参数类型
        params = self._round_params(params)
        _params = {**self.params_bounds, **params}

        # 核心逻辑
        oof = XGBClassifierCV(_params, self.cv, self.cv_seed)
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
    #     rst = xgb.cv(_params,
    #                  self.data,
    #                  num_boost_round=10000,
    #                  nfold=self.cv,
    #                  early_stopping_rounds=300,
    #                  verbose_eval=0,
    #                  show_stdv=False,
    #                  as_pandas=False,
    #                  stratified=True,
    #                  shuffle=True,
    #                  seed=self.cv_seed)
    #
    #     scores = rst['test-auc-mean']
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

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'Optimizer'
__author__ = 'JieYuan'
__mtime__ = '19-3-18'
"""
import numpy as np
from bayes_opt import BayesianOptimization

from ..cv import LGBMClassifierCV


class Optimizer(object):
    """默认LGBMClassifierCV"""

    def __init__(self, X, y, cv=5, cv_seed=0, params_bounds=None):
        """https://www.cnblogs.com/wzdLY/p/9867719.html
        """
        self.X = X
        self.y = y
        self.cv = cv
        self.cv_seed = cv_seed

        self.params_bounds = params_bounds if params_bounds else \
            dict(
                # cat_smooth
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
                reg_alpha=(0, 6),
                reg_lambda=(0, 6),
                n_jobs=-1,
                importance_type='split',  # 'gain'
                verbosity=-1,

                random_state=666,
                bagging_seed=0,
                feature_fraction_seed=0
            )

    def maximize(self, n_iter=3, seed=666, return_best_params=True):
        self.optimizer = BayesianOptimization(
            f=self.objective,
            pbounds={k: v for k, v in self.params_bounds.items() if isinstance(v, tuple)},
            random_state=seed,
            verbose=2
        )
        self.optimizer.maximize(init_points=5, n_iter=n_iter)

        if return_best_params:
            _ = self.optimizer.max
            print(f"Max Score: {_['target']}")
            return self._round_params({**self.params_bounds, **_['params']})

    def objective(self, **params):
        """重写目标函数"""

        # 纠正参数类型
        params = self._round_params(params)
        _params = {**self.params_bounds, **params}
        _params['n_estimators'] = 10000

        # 核心逻辑
        self.clf = LGBMClassifierCV(_params, self.cv, self.cv_seed)
        return self.clf.fit(self.X, self.y, early_stopping_rounds=300, verbose=0)

    def _round_params(self, params):
        for p in ('max_depth', 'depth', 'num_leaves', 'subsample_freq', 'min_child_samples'):
            if p in params:
                params[p] = int(np.round(params[p]))
        return params


if __name__ == '__main__':
    from sklearn.datasets import make_classification

    X, y = make_classification(10000, shift=0.33)
    opt = Optimizer(X, y)
    print(opt.maximize(1))

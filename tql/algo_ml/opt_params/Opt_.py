#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'Optimizer'
__author__ = 'JieYuan'
__mtime__ = '19-3-18'
"""

from sklearn.model_selection import cross_val_score
from bayes_opt import BayesianOptimization
from sklearn import clone
import numpy as np
from functools import partial
from pprint import pprint

from sklearn.model_selection import StratifiedKFold, KFold


class Optimizer(object):

    def __init__(self, estimator=None, pbounds: dict = None):
        """缩小区间长度（边界）
         Notice how we transform between regular and log scale. While this
         is not technically necessary, it greatly improves the performance
         of the optimizer.
        """
        self.estimator = estimator  # sk
        self.pbounds = pbounds
        self.params_type = self._get_params_type(self.pbounds)
        self.scaled_pbounds, self.scaled_params = self._scaler(self.pbounds)
        pprint("Scaled pbounds: %s" % self.scaled_pbounds)

        pprint(self.scaled_pbounds)

    def fit(self, X, y, n_iter=5, feval=None, folds=StratifiedKFold(5, True, 666), oof=True, seed=2019):

        _objective = partial(self.objective, X=X, y=y, oof=oof, feval=feval, folds=folds)
        self.optimizer = BayesianOptimization(
            f=_objective,
            pbounds=self.scaled_pbounds,
            random_state=seed,
            verbose=2
        )

        # gp_params = {"alpha": 1e-5, "n_restarts_optimizer": 3}
        self.optimizer.maximize(n_iter=n_iter)  # self.optimizer.maximize() 可以接着上一次优化继续下一轮优化
        result = self.optimizer.max.copy()
        result['params'] = self._scaler_reverse(result['params'])
        self.best_params = result['params']
        return result

    def objective(self, X, y, oof=True, feval=None, folds=None, **params):
        """cv_score: 核心函数"""
        params = self._scaler_reverse(params)
        estimator = clone(self.estimator)
        estimator.set_params(**params)
        if oof:
            oof = OOF(estimator, folds, verbose=1000)
            oof.fit(X, y, X[:1000], feval)
            cv_score = oof.score
        else:
            cv_score = cross_val_score(estimator, X, y, scoring='roc_auc', cv=5).mean()  # TODO 分数自定义
        return cv_score

    def _get_params_type(self, pbounds):
        _pbounds = pbounds.copy()

        params_type = {}
        for k, v in _pbounds.items():
            params_type.setdefault(str(type(v[0]))[8:-2], []).append(k)
        return params_type

    def _scaler(self, pbounds):
        scaled_params = []
        for k, v in pbounds.items():
            if not -1 <= np.log10(np.ptp(v)) <= 1:  # update pbounds
                scaled_params.append(k)
                pbounds[k] = np.log10(v[0] if v[0] else 1e-6), np.log10(v[1])
        _pbounds = pbounds.copy()

        scaled_params = {'float': [], 'int': [], 'str': []}
        for ps_type, ps in self.params_type.items():
            if ps_type == 'float':
                for p in ps:
                    v = _pbounds[p]
                    if np.ptp(v) / 10 ** -len(str(v[0]).split('.')[1]) > 100:  # 放缩阈值
                        scaled_params['float'].append(p)
                        _pbounds[p] = tuple(np.log10(v))

            if ps_type == 'int':
                for p in ps:
                    v = _pbounds[p]
                    if np.ptp(v) > 256:  # 放缩阈值
                        scaled_params['int'].append(p)
                        _pbounds[p] = tuple(np.log10(v))

            if ps_type == 'str':
                for p in ps:
                    v = _pbounds[p]
                    scaled_params['str'].append(p)
                    _pbounds[p] = (0, len(v) - 1)

        return _pbounds, scaled_params

    def _scaler_reverse(self, params):
        for p in self.scaled_params['float']:
            params[p] = 10 ** params[p]

        for p in self.scaled_params['int']:
            params[p] = int(10 ** params[p])
        for p in self.params_type['int']:
            params[p] = int(params[p])

        for p in self.scaled_params['str']:
            params[p] = self.pbounds[p][int(round(params[p]))]
        return params

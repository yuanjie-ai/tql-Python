#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'xgb'
__author__ = 'JieYuan'
__mtime__ = '19-1-2'
"""

import xgboost as xgb


class   BaselineXGB(object):
    """
    待补充: https://xgboost.readthedocs.io/en/release_0.81/tutorials/feature_interaction_constraint.html
    新版xgb支持交叉特征interaction_constraints
    tree_method='exact'

    b_xgb = BaselineXGB(X, y, learning_rate=0.01)
    b_xgb.run()
    """

    def __init__(self, X, y, learning_rate=0.01, missing=None, metrics='auc', feval=None, objective='binary:logistic',
                 scale_pos_weight=1, n_jobs=8, seed=0):  # seed不能为None
        """
        https://blog.csdn.net/fuqiuai/article/details/79495910
        https://blog.csdn.net/fantacy10000/article/details/84504394
        :param objective:
            'binary:logistic', 'multi:softmax', 'reg:linear'
        :param metrics: string, list of strings or None, optional (default=None)
            binary: 'auc', 'binary_error', 'binary_logloss'
            multiclass: 'multi_error', 'multi_logloss'
            https://lightgbm.readthedocs.io/en/latest/Parameters.html#metric-parameters
        :param feval:
            def feval(y_pred, y_true):
                y_true = y_true.get_label()
                return '1 / (1 + rmse)', 1 /(rmse(y_true, y_pred) + 1), True
        :param scale_pos_weight:
        """
        self.data = xgb.DMatrix(X, y, missing=missing)
        self.objective = objective
        self.metrics = metrics
        self.feval = feval
        self.best_iter = None
        # sklearn params
        self.params_sk = dict(
            booster='gbtree',
            objective=objective,
            max_depth=7,
            learning_rate=learning_rate,

            gamma=0.0,  # 描述分裂的最小 gain, 控制树的有用的分裂
            min_child_weight=1,  # 决定最小叶子节点样本权重和,使一个结点分裂的最小权值之和, 避免过拟合

            subsample=0.8,
            colsample_bytree=0.8,  # 每棵树的列数
            colsample_bylevel=0.8,  # 每一层的列数

            reg_alpha=0.0,
            reg_lambda=0.0,

            scale_pos_weight=scale_pos_weight,

            random_state=seed,
            n_jobs=n_jobs,
            silent=True
        )
        self.params = self.params_sk.copy()

        self.params['eta'] = self.params.pop('learning_rate')
        self.params['alpha'] = self.params.pop('reg_alpha')
        self.params['lambda'] = self.params.pop('reg_lambda')

        if self.objective == 'multi:softmax':
            self.num_class = len(set(y))
            self.params['objective'] = self.objective
            self.params['num_class'] = self.num_class

    def run(self, return_model=False, nfold=5, early_stopping_rounds=100, verbose_eval=50):

        print("XGB CV ...\n")
        try:
            cv_rst = xgb.cv(
                self.params,
                self.data,
                metrics=self.metrics,
                feval=self.feval,
                nfold=nfold,
                num_boost_round=2500,
                stratified=False if 'reg' in self.objective else True,
                early_stopping_rounds=early_stopping_rounds,
                verbose_eval=verbose_eval,
                as_pandas=False
            )
        except TypeError:
            print("Please: self.xgb_data = xgb.DMatrix(data, label=None, missing=None, feature_types=None)")

        if isinstance(self.metrics, str):
            _ = cv_rst['test-%s-mean' % self.metrics]
            self.best_iter = len(_)
            print('\nBest Iter: %s' % self.best_iter)
            print('Best Score: %s ' % _[-1])
        else:
            _ = cv_rst['test-%s-mean' % self.metrics]
            self.best_iter = len(_)
            print('\nBest Iter: %s' % self.best_iter)
            print('Best Score: %s ' % _[-1])

        self.params_sk['n_estimators'] = self.best_iter

        if return_model:
            print("\nReturning Model ...\n")
            return xgb.train(self.params, self.data, self.best_iter)

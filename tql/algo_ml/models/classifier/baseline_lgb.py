#!/usr/bin/env python
# -*- coding= utf-8 -*-
"""
__title__ =  lgb 
__author__ =  JieYuan 
__mtime__ =  19-1-2 
"""

import lightgbm as lgb


class BaselineLGB(object):
    """
    b_lgb = BaselineLGB(X, y, learning_rate=0.01)
    b_lgb.run()
    """

    def __init__(self, X, y, learning_rate=0.01, categorical_feature='auto', metrics='auc', feval=None,
                 objective='binary', scale_pos_weight=1, n_jobs=8, seed=None):
        """
        :param objective:
            Default: 'regression' for LGBMRegressor, 'binary' or 'multiclass' for LGBMClassifier, 'lambdarank' for LGBMRanker.
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
        self.data = lgb.Dataset(X, y, categorical_feature=categorical_feature, free_raw_data=False, weight=None,
                                init_score=None)  # init_score初始分(例如常值/均值/中位数等回归的得分)
        self.objective = objective
        self.metrics = metrics
        self.feval = feval
        self.best_iter = None

        # sklearn params
        self.params_sk = dict(
            metric=self.metrics,
            boosting_type='gbdt',
            objective=objective,
            max_depth=-1,
            num_leaves=17,
            learning_rate=learning_rate,

            min_child_weight=0.001,  # 决定最小叶子节点样本权重和, 孩子节点中最小的样本权重和, 避免过拟合, 如果一个叶子节点的样本权重和小于min_child_weight则拆分过程结束
            min_child_samples=20,  # 一个叶子上数据的最小数量. 可以用来处理过拟合

            subsample=0.8,
            subsample_freq=3,
            colsample_bytree=0.8,

            min_split_gain=0.0,  # 描述分裂的最小 gain, 控制树的有用的分裂
            reg_alpha=0.0,
            reg_lambda=0.0,

            scale_pos_weight=scale_pos_weight,

            random_state=seed,
            n_jobs=n_jobs,
            verbosity=-1  # < 0: Fatal, = 0: Error (Warning), = 1: Info, > 1: Debug
        )
        self.params = self.params_sk.copy()

        if self.objective == 'multiclass':
            self.num_class = len(set(y))
            self.params['objective'] = self.objective
            self.params['num_class'] = self.num_class

    def run(self, return_model=False, nfold=5, early_stopping_rounds=200, verbose_eval=100):

        print("LGB CV ...\n")
        cv_rst = lgb.cv(
            self.params,
            self.data,
            metrics=self.metrics,
            feval=self.feval,
            nfold=nfold,
            num_boost_round=9999,
            stratified=False if 'reg' in self.objective else True,
            early_stopping_rounds=early_stopping_rounds,
            verbose_eval=verbose_eval,
        )

        if isinstance(self.metrics, str):
            _ = cv_rst['%s-mean' % self.metrics]
            self.best_iter = len(_)
        else:
            _ = cv_rst['%s-mean' % self.metrics[0]]
            self.best_iter = len(_)
        print('\nBest Iter: %s' % self.best_iter)
        print('Best Score: %s ' % _[-1])

        self.params_sk['n_estimators'] = self.best_iter

        if return_model:
            print("\nReturning Model ...\n")
            return lgb.train(self.params, self.data, self.best_iter)

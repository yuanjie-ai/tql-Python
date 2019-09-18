#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'opt'
__author__ = 'JieYuan'
__mtime__ = '19-1-3'
"""

"""optuna
https://www.kaggle.com/canonwu/save-intermediate-results-for-stacking/comments

/https://www.cnblogs.com/gczr/p/7156270.html

https://github.com/bamine/Kaggle-stuff/blob/master/otto/hyperopt_xgboost.py#L39
"""

import warnings

warnings.filterwarnings('ignore')
import pandas as pd
import lightgbm as lgb
from bayes_opt import BayesianOptimization
from bayes_opt.observer import JSONLogger
from bayes_opt.event import Events


class BayesOptLGB(object):
    def __init__(self, X, y, metric='auc', objective='binary', categorical_feature='auto', fix_params={}, topk=10,
                 n_jobs=8, opt_seed=None):
        """
        :param X:
        :param y:
        :param metric:
        :param objective: 'regression' , 'binary' or 'multiclass'
        :param categorical_feature:
        :param fix_params:
        :param topk:
        :param opt_seed:
        """

        self.data = lgb.Dataset(X, y, categorical_feature=categorical_feature, silent=True, free_raw_data=False)
        self.metric = metric
        self.objective = objective
        self.topk = topk

        self.fix_params = fix_params
        self.n_jobs = n_jobs
        self.opt_seed = opt_seed

        self.params_ls = []
        self.params_ls_sk = []
        self.params_best = {}
        self.params_best_sk = {}
        self.params_opt_df = None

        self._iter_ls = []

        if self.fix_params:
            print('Fixed Params: \033[94m%s\033[0m\n' % self.fix_params)  # {'min_child_weight': 0.001}

    @property
    def best_model(self):
        if self.params_best:
            return lgb.train(train_set=self.data, **self.params_best)
        else:
            print('\033[94m%s\033[0m\n' % "Please Run !")

    def run(self, n_iter=5, save_log=False):
        BoParams = {
            'num_leaves': (2 ** 4, 2 ** 8),
            'min_split_gain': (0.01, 1),
            'min_child_weight': (0, 0.01),
            'min_child_samples': (8, 32),
            'subsample': (0.6, 1),
            'colsample_bytree': (0.6, 1),
            'reg_alpha': (0, 1),
            'reg_lambda': (0, 1),
        }
        optimizer = BayesianOptimization(self.__evaluator, BoParams, random_state=self.opt_seed)
        if save_log:
            logger = JSONLogger(path="./opt_lgb_logs.json")
            optimizer.subscribe(Events.OPTMIZATION_STEP, logger)

        if self.fix_params:
            optimizer.set_bounds({k: (v, v) for k, v in self.fix_params.items()})

        # optimizer.probe(
        #     {'num_leaves': 2 ** 7 - 1,
        #      'min_split_gain': 0,
        #      'min_child_weight': 0.001,
        #      'min_child_samples': 6,
        #      'subsample': 0.8,
        #      'colsample_bytree': 0.8,
        #      'reg_alpha': 0.01,
        #      'reg_lambda': 1})

        gp_params = {"alpha": 1e-5, "n_restarts_optimizer": 3}
        optimizer.maximize(init_points=3, n_iter=n_iter, acq='ucb', kappa=2.576, xi=0.0, **gp_params)

        self.__get_params(optimizer)

    def __evaluator(self, num_leaves, min_split_gain, min_child_weight, min_child_samples, subsample, colsample_bytree,
                    reg_alpha, reg_lambda):
        self.__params_sk = dict(
            metric=self.metric,
            boosting_type='gbdt',
            objective=self.objective,
            max_depth=-1,
            num_leaves=int(num_leaves),  # 太大会内存泄漏
            learning_rate=0.01,
            min_split_gain=min_split_gain,
            min_child_weight=min_child_weight,
            min_child_samples=int(min_child_samples),
            subsample=subsample,
            subsample_freq=8,
            colsample_bytree=colsample_bytree,
            reg_alpha=reg_alpha,
            reg_lambda=reg_lambda,
            scale_pos_weight=1,
            random_state=0,
            verbosity=-1,
            n_jobs=self.n_jobs
        )
        params = self.__params_sk.copy()
        # params['verbosity'] = -1
        params['metric'] = self.metric

        _ = lgb.cv(params,
                   self.data,
                   num_boost_round=3000,
                   nfold=5,
                   early_stopping_rounds=100,
                   stratified=False if 'reg' in self.objective else True,
                   show_stdv=False)['%s-mean' % self.metric]

        self._iter_ls.append(len(_))
        return -_[-1] if 'reg' in self.objective else _[-1]

    def __get_params(self, optimizer):
        self.params_opt_df = (
            pd.concat([pd.DataFrame({'iter': self._iter_ls}), pd.DataFrame(optimizer.res)], 1)
                .sort_values('target', ascending=False)
                .reset_index(drop=True)[:self.topk])

        for _, (i, _, p) in self.params_opt_df.iterrows():
            params_sk = {**self.__params_sk, **p, **{'n_estimators': i}}

            params_sk['num_leaves'] = int(params_sk['num_leaves'])
            params_sk['min_child_samples'] = int(params_sk['min_child_samples'])
            params_sk = {k: float('%.3f' % v) if isinstance(v, float) else v for k, v in params_sk.items()}
            self.params_ls_sk.append(params_sk)

            params = params_sk.copy()
            num_boost_round = params.pop('n_estimators')
            self.params_ls.append({'params': params, 'num_boost_round': num_boost_round})

        self.params_best = self.params_ls[0]
        self.params_best_sk = self.params_ls_sk[0]

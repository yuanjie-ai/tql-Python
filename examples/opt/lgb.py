#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : lgb
# @Time         : 2019-09-16 10:06
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

from tql.algo_ml.cv import LGBMClassifierCV
from tql.algo_ml.opt_params import Optimizer
from sklearn.datasets import make_classification

X, y = make_classification(10000)


class Opt(Optimizer):

    def objective(self, **params):
        """重写目标函数"""
        self.params = params
        # 超参
        params['num_leaves'] = int(params['num_leaves'])
        params['min_child_samples'] = int(params['min_child_samples'])

        # 固定参数：TODO 更方便的方式
        params['n_estimators'] = 3000
        params['subsample_freq'] = 6  # 需要调参不
        params['verbosity'] = -1
        params['n_jobs'] = 16

        # self.params = params
        self.clf = LGBMClassifierCV(params)
        return self.clf.fit(X, y, X[:1])


opt = Optimizer(X, y)
print(opt.maximize(1))

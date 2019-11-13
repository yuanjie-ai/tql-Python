#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : demo
# @Time         : 2019-09-16 14:17
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :


from tql.algo_ml.opt_params import LGBMOptimizer, XGBOptimizer, CatBoostOptimizer, Optimizer

from sklearn.datasets import make_classification

X, y = make_classification(1000)

# opt = Optimizer(X, y, cv=5, cv_seed=0)
# print(opt.maximize(1))

opt = LGBMOptimizer(X, y, cv=5, cv_seed=0)
print(opt.maximize(1))
print(len(opt.res))
print(len(opt.optimizer.max))


# opt = XGBOptimizer(X, y, cv=5, cv_seed=0, use_gpu=0)
# print(opt.maximize(1))
#
# opt = CatBoostOptimizer(X, y, cv=5, cv_seed=0, use_gpu=0)
# print(opt.maximize(1))

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : demo
# @Time         : 2019-09-16 14:17
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


from tql.algo_ml.opt_params import LGBMOptimizer

from sklearn.datasets import make_classification

X, y = make_classification(1000)
opt = LGBMOptimizer(X, y, cv=5, random_state=555)

print(opt.maximize(1))

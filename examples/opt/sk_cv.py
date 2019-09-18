#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : sk_cv
# @Time         : 2019-09-16 11:32
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


from sklearn.datasets import make_classification
from tql.algo_ml.opt_params import Optimizer
X, y = make_classification(
    n_samples=1000,
    n_features=45,
    n_informative=12,
    n_redundant=7,
    random_state=134985745,
)


opt = Optimizer(X, y)
print(opt.maximize(1))

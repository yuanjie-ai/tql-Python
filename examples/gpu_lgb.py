#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : gpu_lgb
# @Time         : 2019-07-04 12:14
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

"""默认参数https://www.kaggle.com/c/home-credit-default-risk/discussion/59347#latest-542068"""
import lightgbm as lgb

from sklearn.datasets import make_classification


X, y = make_classification(10000)
param = {
    'num_leaves': 10,
    'max_bin': 127,
    'min_data_in_leaf': 11,
    'learning_rate': 0.02,
    'min_sum_hessian_in_leaf': 0.00245,
    'bagging_fraction': 1.0,
    'bagging_freq': 5,
    'feature_fraction': 0.05,
    'lambda_l1': 4.972,
    'lambda_l2': 2.276,
    'min_gain_to_split': 0.65,
    'max_depth': 14,
    'save_binary': True,
    'seed': 1337,
    'feature_fraction_seed': 1337,
    'bagging_seed': 1337,
    'drop_seed': 1337,
    'data_random_seed': 1337,
    'objective': 'binary',
    'boosting_type': 'gbdt',
    'verbose': 1,
    'metric': 'auc',
    'is_unbalance': True,
    'boost_from_average': False,
    'device': 'gpu',
    'gpu_platform_id': 0,
    'gpu_device_id': 0,
    'gpu_use_dp':True
}

data = lgb.Dataset(X, y)
_ = lgb.cv(param, data, num_boost_round=10000, verbose_eval=1000)

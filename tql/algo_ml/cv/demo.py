#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : demo
# @Time         : 2019-09-28 10:51
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

from tql.algo_ml.cv import LGBMClassifierCV

from sklearn.datasets import make_classification

X, y = make_classification(1000)

params = {
    # 'metric': 'auc',
    'boosting_type': 'gbdt',
    'objective': 'binary',
    'max_depth': -1,
    'num_leaves': 16,
    'learning_rate': 0.005,
    'min_split_gain': 0.884,
    'min_child_weight': 0.01,
    'min_child_samples': 31,
    'subsample': 0.788,
    'subsample_freq': 8,
    'colsample_bytree': 0.617,
    'reg_alpha': 0.631,
    'reg_lambda': 0.81,
    'scale_pos_weight': 1,
    'verbosity': -1,
    'n_jobs': 30,
    'n_estimators': 30000,

    'random_state': 666,
    'bagging_seed': 0,
    'feature_fraction_seed': 0,
}


# 原生接口
# params['init_model'] = oof.clf
# params['keep_training_booster']=True
oof = LGBMClassifierCV(params)
oof.fit(X, y, X, eval_metric=('auc'))

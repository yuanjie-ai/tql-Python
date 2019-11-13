#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : params
# @Time         : 2019-09-25 17:05
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


params_lgb = {
    'n_estimators': 10000,
    'metric': 'auc',
    'boosting_type': 'gbdt',
    'objective': 'binary',
    'max_depth': -1,
    'num_leaves': 16,
    'learning_rate': 0.005,

    'subsample': 0.788,
    'subsample_freq': 8,
    'colsample_bytree': 0.617,

    'reg_alpha': 0.631,
    'reg_lambda': 0.81,
    'min_split_gain': 0.884,
    'min_child_weight': 0.01,
    'min_child_samples': 31,

    'n_jobs': -1,
    'verbosity': -1,
    'scale_pos_weight': 1,

    'random_state': 666,
    'bagging_seed': 0,
    'feature_fraction_seed': 0,
}

params_xgb = {
    'n_estimators': 10000,
    'eval_metric': 'auc',
    'booster': 'gbtree',
    'objective': 'binary:logistic',
    'max_depth': 7,
    'learning_rate': 0.02421306293966501,

    'subsample': 0.5795222896954795,
    'colsample_bytree': 0.19985830478870198,
    'colsample_bylevel': 1,

    'reg_alpha': 5.455077557037526,
    'reg_lambda': 5.8700819100907715,

    'gamma': 0.2484205604663352,
    'min_child_weight': 19.75111813614344,
    'max_delta_step': 1.4546423084703382,

    'n_jobs': -1,
    'verbosity': 0,
    'scale_pos_weight': 1,

    'tree_method': 'gpu_hist',
    'predictor': 'gpu_predictor',
    'random_state': 666
}

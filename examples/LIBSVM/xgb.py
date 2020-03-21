#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : xgb
# @Time         : 2020-02-06 19:13
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

import os
import sys
import xgboost  as xgb

print(sys.argv)
if len(sys.argv) == 3:
    train_path, test_path = sys.argv[1:]
else:
    raise Exception("请指定训练集与测试集路径")
p = "/Users/yuanjie/Desktop/libsvm.csv"

params = {
    'booster': 'gbtree',
    'objective': 'binary:logistic',
    'eta': 0.1,
    'max_depth': 6,

    'gamma': 0,
    'min_child_weight': 1,

    'subsample': 0.8,
    'colsample_bytree': 0.8,
    'alpha': 0,
    'lambda': 1,

    'scale_pos_weight': 1,
    'eval_metric': 'auc',
    'nthread': 8,
    'seed': 888,
}

if __name__ == '__main__':
    # dtrain = xgb.DMatrix(f'{train_path}#dtrain.cache')
    # xgb.cv(
    #     params,
    #     dtrain,
    #     num_boost_round=2000,
    #     nfold=3,
    #     stratified=True,
    #     early_stopping_rounds=50,
    #     verbose_eval=100,
    #     seed=0
    # )

    dtrain = xgb.DMatrix(f'{train_path}#dtrain.cache')
    dtest = xgb.DMatrix(f'{test_path}#dtest.cache')
    watchlist = [(dtrain, 'train'), (dtest, 'test')]

    bst = xgb.train(params, dtrain, 300, watchlist, verbose_eval=50, early_stopping_rounds=50)
    bst.save_model('./xgb_booster.bin')
    bst.dump_model('./dump.raw.txt')

    # del
    os.system("rm *cache*")

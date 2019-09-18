#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : xgboost_gpu
# @Time         : 2019-07-03 14:31
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

"""
xgb/lgb 参数https://www.jianshu.com/p/1100e333fcab
"""
from xgboost import XGBClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

X, y = make_classification(100000)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.33, random_state=42)


clf = XGBClassifier(learning_rate=0.01,
                    n_estimators=10000,
                    tree_method='gpu_hist',
                    predictor='gpu_predictor',
                    verbosity=0,
                    n_jobs=8,
                   )

clf.fit(X, y,
        eval_metric='auc',
        eval_set=[(X_train, y_train), (X_test, y_test)],
        early_stopping_rounds=300,
        verbose=100)

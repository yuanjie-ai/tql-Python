#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : gpu_catb
# @Time         : 2019-07-04 13:27
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


from catboost import CatBoostClassifier
from sklearn.datasets import make_classification

X, y = make_classification(100000)

# 支持字符串类别
# object 无需数值化直接 train
# cats = X.dtypes[X.dtypes == object].index
# for i in cats:
#     X[i] = X[i].astype(str)
model = CatBoostClassifier(
    loss_function="Logloss",
    eval_metric="AUC",
    learning_rate=0.05,
    n_estimators=10000,
    l2_leaf_reg=50,
    random_seed=666,
    od_type="Iter",
    depth=5,
    early_stopping_rounds=100,
    border_count=64,
    has_time=True,
    verbose=0,
    thread_count=30,
    task_type="GPU",
)

model.fit(X, y, eval_set=(X, y), verbose=1000, use_best_model=True, plot=True)
from sklearn.ensemble import StackingClassifier

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'example'
__author__ = 'JieYuan'
__mtime__ = '19-2-18'
"""
import numpy as np
from hyperopt import fmin, hp, tpe, Trials, STATUS_OK
from hyperopt.pyll import scope
import lightgbm as lgb
from sklearn.datasets import load_iris

N_FOLDS = 5
bayes_trials = Trials()
X, y = load_iris(True)
# Create the dataset
train_set = lgb.Dataset(X[:100], y[:100])


def objective(params, n_folds=N_FOLDS):
    """Objective function for Gradient Boosting Machine Hyperparameter Tuning"""

    # Perform n_fold cross validation with hyperparameters
    # Use early stopping and evalute based on ROC AUC
    params['verbosity'] = -1
    cv_results = lgb.cv(params, train_set, nfold=n_folds, num_boost_round=10000, early_stopping_rounds=100,
                        metrics='auc', seed=50, verbose_eval=50)
    # 此部分为核心代码，

    # Extract the best score
    best_score = max(cv_results['auc-mean'])
    # Loss must be minimized
    loss = 1 - best_score

    # Dictionary with information for evaluation
    return {'loss': loss, 'params': params, 'status': STATUS_OK}


# Define the search space
space = {
    'num_leaves': scope.int(hp.quniform('num_leaves', 2 ** 4, 2 ** 8, 1)),
    'learning_rate': hp.loguniform('learning_rate', np.log(1e-5), np.log(1)),

    'min_child_weight': hp.uniform('min_child_weight', 0, 0.01),
    'min_child_samples': scope.int(hp.quniform('min_child_samples', 8, 32, 2)),

    # 采样
    'subsample': hp.uniform('subsample', 0.5, 1),
    'subsample_freq': scope.int(hp.quniform('subsample_freq', 1, 5, 1)),
    'colsample_bytree': hp.uniform('colsample_by_tree', 0.5, 1.0),
    # 正则
    'min_split_gain': hp.uniform('min_split_gain', 0, 1),
    'reg_alpha': hp.loguniform('reg_alpha', np.log(1e-5), np.log(1e5)),
    'reg_lambda': hp.loguniform('reg_lambda', np.log(1e-5), np.log(1e5)),
}

MAX_EVALS = 100

# Optimize
best = fmin(fn=objective, space=space, algo=tpe.suggest,
            max_evals=MAX_EVALS, trials=bayes_trials, verbose=1)


print(bayes_trials)



# xgb
# space = {
#     'n_estimators': hp.quniform('n_estimators', 100, 1000, 1),
#     'eta': hp.quniform('eta', 0.025, 0.5, 0.025),
#     'max_depth': hp.quniform('max_depth', 1, 13, 1),
#     'min_child_weight': hp.quniform('min_child_weight', 1, 6, 1),
#     'subsample': hp.quniform('subsample', 0.5, 1, 0.05),
#     'gamma': hp.quniform('gamma', 0.5, 1, 0.05),
#     'colsample_bytree': hp.quniform('colsample_bytree', 0.5, 1, 0.05),
#     'num_class': 9,
#     'eval_metric': 'mlogloss',
#     'objective': 'multi:softprob',
#     'nthread': 6,
#     'silent': 1
# }

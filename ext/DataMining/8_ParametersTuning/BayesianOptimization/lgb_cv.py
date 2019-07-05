# coding: utf-8
__title__ = 'xgboost_cv'
__author__ = 'JieYuan'
__mtime__ = '2017/11/5'

import warnings

warnings.filterwarnings('ignore')
import numpy as np
import lightgbm as lgb
from sklearn.datasets import make_classification
from bayes_opt import BayesianOptimization

X, y = make_classification(
    n_samples=1000,
    n_features=45,
    n_informative=12,
    n_redundant=7
)
train_set = lgb.Dataset(X, y)

def evaluator(max_depth, min_split_gain, min_child_weight, bagging_fraction, feature_fraction, lambda_l1,
              lambda_l2):
    params = {
        'boosting': 'gbdt',
        'application': 'binary',
        'learning_rate': 0.01,
        'max_depth': -1,
        'num_leaves': 2 ** int(max_depth),
        'min_split_gain': min_split_gain,
        'min_child_weight': min_child_weight,
        'bagging_fraction': bagging_fraction,
        'feature_fraction': feature_fraction,
        'lambda_l1': lambda_l1,
        'lambda_l2': lambda_l2,
        'scale_pos_weight': 1,
        'num_threads': -1,
    }

    metrics = 'auc'  # 定义评估函数
    cv_result = lgb.cv(params,
                       train_set,
                       num_boost_round=1000,
                       nfold=3,
                       stratified=True,
                       metrics=metrics,
                       early_stopping_rounds=10,
                       verbose_eval=50,
                       show_stdv=False,
                       seed=0)
    return cv_result[metrics + '-mean'][-1]

# test
# evaluator(3, 1, 1, 1, 1, 1, 1)

BoParams = {
    'max_depth': (6, 11),
    'min_split_gain': (0.05, 1),
    'min_child_weight': (1, 10),
    'bagging_fraction': (0.6, 1),
    'feature_fraction': (0.6, 1),
    'lambda_l1': (0, 10),
    'lambda_l2': (0, 10),
}
BO = BayesianOptimization(evaluator, BoParams)
gp_params = {"alpha": 1e-5, "n_restarts_optimizer": 2}
BO.maximize(init_points=5, n_iter=25, acq='ucb', kappa=2.576, xi=0.0, **gp_params) # kappa??? **gp_params可能报错
BO.res['max']


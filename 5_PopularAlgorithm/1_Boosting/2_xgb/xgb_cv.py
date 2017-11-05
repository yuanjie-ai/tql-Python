# coding: utf-8
__title__ = 'xgboost_cv'
__author__ = 'JieYuan'
__mtime__ = '2017/11/5'

import warnings

warnings.filterwarnings('ignore')
import numpy as np
import xgboost as xgb
from sklearn.datasets import make_classification
from bayes_opt import BayesianOptimization

X, y = make_classification(
    n_samples=1000,
    n_features=45,
    n_informative=12,
    n_redundant=7
)
train_set = xgb.DMatrix(X, y)

def evaluator(max_depth, min_split_gain, min_child_weight, bagging_fraction, feature_fraction, lambda_l1,
              lambda_l2):
    params = {
        'booster': 'gbtree',
        'objective': 'binary:logistic',
        'eta': 0.01,
        'max_depth': int(max_depth),
        'gamma': min_split_gain,
        'min_child_weight': min_child_weight,
        'subsample': bagging_fraction,
        'colsample_bytree': feature_fraction,
        'alpha': lambda_l1,
        'lambda': lambda_l2,
        'scale_pos_weight': 1,
        'nthread': 8
    }

    metrics = 'auc'  # 定义评估函数
    cv_result = xgb.cv(params,
                       train_set,
                       num_boost_round=20,
                       nfold=3,
                       stratified=True,
                       metrics=metrics,
                       early_stopping_rounds=5,
                       verbose_eval=5,
                       show_stdv=True,
                       seed=0)
    return cv_result['test-' + metrics + '-mean'].mean()

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
BO.maximize()
BO.res['max']

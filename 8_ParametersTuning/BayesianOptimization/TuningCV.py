# coding: utf-8
__title__ = 'byes'
__author__ = 'JieYuan'
__mtime__ = '2017/12/10'

import warnings

warnings.filterwarnings('ignore')
from udfs import *
import lightgbm as lgb
import xgboost as xgb

from bayes_opt import BayesianOptimization
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

# load data
from sklearn.datasets import make_classification
X, y = make_classification(
    n_samples=1000,
    n_features=45,
    n_informative=12,
    n_redundant=7
)

class BayesOpt(object):
    def __init__(self):
        pass

    @staticmethod
    def lgb():
        BoParams = {
            'max_depth': (6, 11),
            'min_split_gain': (0.05, 1),
            'min_child_weight': (1, 10),
            'bagging_fraction': (0.6, 1),
            'feature_fraction': (0.6, 1),
            'lambda_l1': (0, 100),
            'lambda_l2': (0, 100),
        }
        train_set = lgb.Dataset(X, y)
        BO = BayesianOptimization(_lgb_loss, BoParams)
        BO.maximize(init_points=5, n_iter=10, acq='ucb', kappa=2.576, xi=0.0)
        print(BO.res['max'])
        return BO.res

    @staticmethod
    def xgb():
        BoParams = {
            'max_depth': (6, 11),
            'min_split_gain': (0.05, 1),
            'min_child_weight': (1, 10),
            'bagging_fraction': (0.6, 1),
            'feature_fraction': (0.6, 1),
            'lambda_l1': (0, 100),
            'lambda_l2': (0, 100),
        }
        train_set = xgb.DMatrix(X, y)
        BO = BayesianOptimization(_xgb_loss, BoParams)
        BO.maximize(init_points=5, n_iter=10, acq='ucb', kappa=2.576, xi=0.0)
        print(BO.res['max'])
        return BO.res

    @staticmethod
    def rf():
        BoParams = {
            'n_estimators': (120, 1200),
            'max_depth': (6, 30),
            'min_samples_split': (1, 100),
            'min_samples_leaf': (1, 10),
        }
        BO = BayesianOptimization(_rf_loss, BoParams)
        BO.maximize(init_points=5, n_iter=10, acq='ucb', kappa=2.576, xi=0.0)
        print(BO.res['max'])
        return BO.res

    @staticmethod
    def gbdt():
        BoParams = {
            'n_estimators': (100, 2000),
            'max_depth': (6, 15),
            'subsample': (0.6, 1),
        }
        BO = BayesianOptimization(_gbdt_loss, BoParams)
        BO.maximize(init_points=5, n_iter=10, acq='ucb', kappa=2.576, xi=0.0)
        print(BO.res['max'])
        return BO.res





# lgb
def _lgb_loss(max_depth, min_split_gain, min_child_weight, bagging_fraction, feature_fraction, lambda_l1, lambda_l2):
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
    metrics = 'auc'
    cv_result = lgb.cv(params,
                       train_set,
                       num_boost_round=1000,
                       nfold=3,
                       stratified=True,
                       metrics='auc',
                       early_stopping_rounds=10,
                       verbose_eval=50,
                       show_stdv=False,
                       seed=0)
    return cv_result[metrics + '-mean'][-1]

# xgb
def _xgb_loss(max_depth, min_split_gain, min_child_weight, bagging_fraction, feature_fraction, lambda_l1, lambda_l2):
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
        'nthread': -1
    }

    metrics = 'auc'  # 定义评估函数
    cv_result = xgb.cv(params,
                       train_set,
                       num_boost_round=1000,
                       nfold=3,
                       stratified=True,
                       metrics=metrics,
                       early_stopping_rounds=10,
                       verbose_eval=50,
                       show_stdv=True,
                       seed=0)
    return cv_result['test-' + metrics + '-mean'].mean()

# rf
def _rf_loss(n_estimators, max_depth, min_samples_split, min_samples_leaf):
    clf = RandomForestClassifier(n_estimators=int(n_estimators),
                                 max_depth=int(max_depth),  # 5, 8, 15, 25, 30
                                 criterion='gini',  # 'entropy'
                                 min_samples_split=int(min_samples_split),  # 1, 2, 5, 10, 15, 100
                                 min_samples_leaf=int(min_samples_leaf),  # 1, 2, 5, 10
                                 max_features='auto',
                                 n_jobs=-1,
                                 random_state=42)
    scores = cross_val_score(clf, X, y, cv=3, scoring='roc_auc')
    return scores.mean()

# gbdt
def _gbdt_loss(n_estimators, max_depth, subsample):
    clf = RandomForestClassifier(n_estimators=int(n_estimators),
                                 max_depth=int(max_depth),
                                 learning_rate=0.01,
                                 min_samples_split=2,
                                 min_samples_leaf=1,
                                 subsample=subsample,
                                 max_features='auto',
                                 random_state=42)
    scores = cross_val_score(clf, X, y, cv=3, scoring='roc_auc')
    return scores.mean()

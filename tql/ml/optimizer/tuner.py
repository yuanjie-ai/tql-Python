#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : LGBMClassifierTuner
# @Time         : 2020/9/21 10:19 上午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


import optuna
import numpy as np
import pandas as pd

import xgboost as xgb
import lightgbm as lgb
import catboost as catb

from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from sklearn.metrics import roc_auc_score

from tql.ml.oof.oofs import LGBMClassifierOOF, XGBClassifierOOF, CatBoostClassifierOOF
from tql.ml.optimizer.BaseOptimizer import BaseOptimizer


# CatBoostClassifier(loss_function="Logloss",
#                            eval_metric="AUC",
#                            task_type="GPU",
#                            learning_rate=0.05,
#                            n_estimators=10000,
#                            l2_leaf_reg=50,
#                            random_seed=666,
#                            od_type="Iter",
#                            depth=5,
#                            early_stopping_rounds=100,
#                            border_count=64,
#                            has_time=True
#                            )

class CatBoostClassifierTuner(BaseOptimizer):  # TODO：调整参数名
    # _process_synonyms_group(['learning_rate', 'eta'], params)
    # _process_synonyms_group(['border_count', 'max_bin'], params)
    # _process_synonyms_group(['depth', 'max_depth'], params)
    # _process_synonyms_group(['rsm', 'colsample_bylevel'], params)
    # _process_synonyms_group(['random_seed', 'random_state'], params)
    # _process_synonyms_group(['l2_leaf_reg', 'reg_lambda'], params)
    # _process_synonyms_group(['iterations', 'n_estimators', 'num_boost_round', 'num_trees'], params)
    # _process_synonyms_group(['od_wait', 'early_stopping_rounds'], params)
    # _process_synonyms_group(['custom_metric', 'custom_loss'], params)
    # _process_synonyms_group(['max_leaves', 'num_leaves'], params)
    # _process_synonyms_group(['min_data_in_leaf', 'min_child_samples'], params)

    def __init__(self, X, y, params=None, feval=roc_auc_score):
        self.X = X
        self.y = y
        self.params = params  #
        self.feval = feval

    def _objective(self, trial: optuna.trial.Trial):
        cv = trial.suggest_int('cv', 2, 2 ** 4)

        opt_params = dict(
            objective=trial.suggest_categorical("objective", ["Logloss", "CrossEntropy"]),
            boosting_type=trial.suggest_categorical("boosting_type", ["Ordered", "Plain"]),
            bootstrap_type=trial.suggest_categorical("bootstrap_type", ["Bayesian", "Bernoulli", "MVS"]),
            # used_ram_limit="3gb",

            max_depth=trial.suggest_int("max_depth", 2, 2 ** 4),
            learning_rate=trial.suggest_discrete_uniform('learning_rate', 0.001, 1, 0.001),
            # n_estimators=trial.suggest_int("n_estimators", 2, 2 ** 10, log=True),

            colsample_bylevel=trial.suggest_float("colsample_bylevel", 0.01, 0.1),
            reg_lambda=trial.suggest_float("reg_lambda", 1e-8, 100, log=True)

        )

        if opt_params["bootstrap_type"] == "Bayesian":
            opt_params["bagging_temperature"] = trial.suggest_float("bagging_temperature", 0, 10)
        elif opt_params["bootstrap_type"] == "Bernoulli":
            opt_params["subsample"] = trial.suggest_float("subsample", 0.1, 1)

        if self.params is not None:
            opt_params.update(self.params)

        clf_oof = CatBoostClassifierOOF(self.X, self.y, params=opt_params, cv=cv, feval=self.feval)
        clf_oof.run()

        return clf_oof.oof_score  # todo: f1

    def best_params(self):
        if self.params is not None:
            return {**self.study.best_params, **self.params}
        else:
            return self.study.best_params


class XGBTuner(BaseOptimizer):

    def __init__(self, X, y, params=None, feval=roc_auc_score):
        self.X = X
        self.y = y
        self.dtrain = xgb.DMatrix(self.X, self.y, silent=True)

        self.params = params
        self.feval = feval

    def _objective(self, trial: optuna.trial.Trial):
        cv = trial.suggest_int('cv', 2, 2 ** 4)
        opt_params = dict(
            booster=trial.suggest_categorical("booster", ["gbtree", "gblinear", "dart"]),

            min_child_weight=trial.suggest_float('min_child_weight', 1e-8, 2 ** 10, log=True),

            subsample=trial.suggest_float('subsample', 0.1, 1),
            colsample_bytree=trial.suggest_float('colsample_bytree', 0.1, 1),
            colsample_bylevel=trial.suggest_float('colsample_bylevel', 0.1, 1),

            alpha=trial.suggest_float('alpha', 1e-8, 10, log=True),
            # reg_lambda=trial.suggest_loguniform('reg_lambda', 1e-8, 10),
        )
        opt_params['lambda'] = trial.suggest_float('lambda', 1e-8, 10, log=True)

        if opt_params["booster"] == "gbtree" or opt_params["booster"] == "dart":
            opt_params["max_depth"] = trial.suggest_int("max_depth", 2, 2 ** 4)
            opt_params["gamma"] = trial.suggest_float("gamma", 1e-8, 1.0, log=True)
            opt_params["grow_policy"] = trial.suggest_categorical("grow_policy", ["depthwise", "lossguide"])
        if opt_params["booster"] == "dart":
            opt_params["sample_type"] = trial.suggest_categorical("sample_type", ["uniform", "weighted"])
            opt_params["normalize_type"] = trial.suggest_categorical("normalize_type", ["tree", "forest"])
            opt_params["rate_drop"] = trial.suggest_float("rate_drop", 1e-8, 1.0, log=True)
            opt_params["skip_drop"] = trial.suggest_float("skip_drop", 1e-8, 1.0, log=True)

        if self.params is not None:
            opt_params.update(self.params)

        cv_result = xgb.cv(
            opt_params,
            self.dtrain,
            num_boost_round=10000,
            nfold=cv,
            stratified='reg' not in opt_params['objective'],
            feval=None, maximize=False,
            verbose_eval=100,
            early_stopping_rounds=100,

            as_pandas=True,
            show_stdv=True,
            seed=0,
        )

        score = cv_result.iloc[:, -2].tolist()[-1]

        self.best_num_boost_round = len(cv_result)

        return score

    def best_params(self):
        if self.params is not None:
            return {**self.study.best_params, **self.params}
        else:
            return self.study.best_params


class XGBClassifierTuner(BaseOptimizer):

    def __init__(self, X, y, params=None, feval=roc_auc_score):
        self.X = X
        self.y = y
        self.params = params
        self.feval = feval

    def _objective(self, trial: optuna.trial.Trial):
        cv = trial.suggest_int('cv', 2, 2 ** 4)
        opt_params = dict(
            max_depth=trial.suggest_int("max_depth", 2, 2 ** 4),
            learning_rate=trial.suggest_float('learning_rate', 0.001, 1, step=0.001),
            # n_estimators=trial.suggest_int("n_estimators", 2, 2 ** 10, log=True),

            gamma=trial.suggest_float('gamma', 1e-8, 1, log=True),
            min_child_weight=trial.suggest_float('min_child_weight', 1e-8, 2 ** 10, log=True),

            subsample=trial.suggest_float('subsample', 0.1, 1),
            colsample_bytree=trial.suggest_float('colsample_bytree', 0.1, 1),
            colsample_bylevel=trial.suggest_float('colsample_bylevel', 0.1, 1),

            reg_alpha=trial.suggest_float('reg_alpha', 1e-8, 10, log=True),
            reg_lambda=trial.suggest_float('reg_lambda', 1e-8, 10, log=True),
        )

        if self.params is not None:
            opt_params.update(self.params)

        clf_oof = XGBClassifierOOF(self.X, self.y, params=opt_params, cv=cv, feval=self.feval)
        clf_oof.run()

        return clf_oof.oof_score  # todo: f1

    def best_params(self):
        if self.params is not None:
            return {**self.study.best_params, **self.params}
        else:
            return self.study.best_params


class LGBTuner(BaseOptimizer):
    def __init__(self, X, y, params=None, feval=roc_auc_score):
        self.X = X
        self.y = y
        self.dtrain = lgb.Dataset(self.X, self.y, silent=True)

        self.params = params
        self.feval = feval

    def _objective(self, trial: optuna.trial.Trial):
        cv = trial.suggest_int('cv', 2, 2 ** 4)
        opt_params = dict(
            num_leaves=trial.suggest_int("num_leaves", 2, 2 ** 8),
            learning_rate=trial.suggest_float('learning_rate', 0.001, 1, step=0.001),

            min_child_samples=trial.suggest_int('min_child_samples', 2, 2 ** 8),
            min_child_weight=trial.suggest_float('min_child_weight', 1e-8, 1, log=True),
            min_split_gain=trial.suggest_float('min_split_gain', 1e-8, 1, log=True),

            bagging_fraction=trial.suggest_float('bagging_fraction', 0.4, 1),
            bagging_freq=trial.suggest_int("bagging_freq", 0, 2 ** 4),
            feature_fraction=trial.suggest_float('feature_fraction', 0.4, 1),

            lambda_l1=trial.suggest_float('lambda_l1', 1e-8, 10, log=True),
            lambda_l2=trial.suggest_float('lambda_l2', 1e-8, 10, log=True),
        )

        if self.params is not None:
            opt_params.update(self.params)

        cv_result = lgb.cv(
            opt_params,
            self.dtrain,
            num_boost_round=10000,
            nfold=cv,
            stratified='reg' not in opt_params.get('application', opt_params.get('objective', 'reg')),
            feval=None,
            early_stopping_rounds=100,
            verbose_eval=100,
            show_stdv=False,
            seed=0,
            eval_train_metric=False
        )

        score = -1
        self.best_num_boost_round = 0
        for key in cv_result:
            if 'mean' in key:
                _ = cv_result[key]
                score = _[-1]
                self.best_num_boost_round = len(_)

        print(f'CV Score: {score if score != -1 else "cv_result donot contain mean-metric"}')

        return score

    def best_params(self):
        if self.params is not None:
            return {**self.study.best_params, **self.params}
        else:
            return self.study.best_params


class LGBMClassifierTuner(BaseOptimizer):

    def __init__(self, X, y, params=None, feval=roc_auc_score):
        self.X = X
        self.y = y
        self.params = params
        self.feval = feval

    def _objective(self, trial: optuna.trial.Trial):
        cv = trial.suggest_int('cv', 2, 2 ** 4)
        opt_params = dict(
            num_leaves=trial.suggest_int("num_leaves", 2, 2 ** 8),
            learning_rate=trial.suggest_float('learning_rate', 0.001, 1, step=0.001),
            # n_estimators=trial.suggest_int("n_estimators", 2, 2 ** 10, log=True),

            min_child_samples=trial.suggest_int('min_child_samples', 2, 2 ** 8),
            min_child_weight=trial.suggest_float('min_child_weight', 1e-8, 1, log=True),
            min_split_gain=trial.suggest_float('min_split_gain', 1e-8, 1, log=True),

            subsample=trial.suggest_float('subsample', 0.4, 1),
            subsample_freq=trial.suggest_int("subsample_freq", 0, 2 ** 4),
            colsample_bytree=trial.suggest_float('colsample_bytree', 0.4, 1),

            reg_alpha=trial.suggest_float('reg_alpha', 1e-8, 10, log=True),
            reg_lambda=trial.suggest_float('reg_lambda', 1e-8, 10, log=True),
        )

        if self.params is not None:
            opt_params.update(self.params)

        clf_oof = LGBMClassifierOOF(self.X, self.y, params=opt_params, cv=cv, feval=self.feval)
        clf_oof.run()

        return clf_oof.oof_score  # todo: f1

    def best_params(self):
        if self.params is not None:
            return {**self.study.best_params, **self.params}
        else:
            return self.study.best_params

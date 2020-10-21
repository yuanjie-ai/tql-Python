#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tuning.
# @File         : models
# @Time         : 2020/9/4 4:04 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : https://www.kaggle.com/isaienkov/top-10-efficient-ensembling-in-few-lines-of-code


import sklearn
import optuna
from sklearn.ensemble import *
from lightgbm import LGBMClassifier
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier
from catboost import CatBoostClassifier


class ModelZoo(object):

    def __init__(self, model_name="RandomForestClassifier",
                 higher_is_better=True,
                 params={'random_state': 666, 'n_jobs': 8}):
        self.model_name = model_name
        self.higher_is_better = higher_is_better
        self.params = params  # 精简调参，也可以通过parms覆盖/固定参数

    def __call__(self, trial: optuna.trial.Trial):
        return self.__getattribute__(f"model{self.model_name}")(trial)

    def modelLGBMClassifier(self, trial: optuna.trial.Trial):
        opt_params = dict(
            num_leaves=trial.suggest_int("num_leaves", 2, 2 ** 8),
            learning_rate=trial.suggest_discrete_uniform('learning_rate', 0.001, 1, 0.001),
            n_estimators=trial.suggest_int("n_estimators", 2, 2 ** 10, log=True),

            min_child_samples=trial.suggest_int('min_child_samples', 2, 2 ** 8),
            min_child_weight=trial.suggest_loguniform('min_child_weight', 1e-8, 1),
            min_split_gain=trial.suggest_loguniform('min_split_gain', 1e-8, 1),

            subsample=trial.suggest_uniform('subsample', 0.4, 1),
            subsample_freq=trial.suggest_int("subsample_freq", 0, 2 ** 4),
            colsample_bytree=trial.suggest_uniform('colsample_bytree', 0.4, 1),
            reg_alpha=trial.suggest_loguniform('reg_alpha', 1e-8, 10),
            reg_lambda=trial.suggest_loguniform('reg_lambda', 1e-8, 10),
        )
        clf = LGBMClassifier(
            boosting_type='gbdt',
            num_leaves=31,
            max_depth=-1,
            learning_rate=0.1,
            n_estimators=100,
            subsample_for_bin=200000,
            objective=None,
            class_weight=None,
            min_split_gain=0.,
            min_child_weight=1e-3,
            min_child_samples=20,
            subsample=1.,
            subsample_freq=0,
            colsample_bytree=1.,
            reg_alpha=0.,
            reg_lambda=0.,
            random_state=None,
            n_jobs=-1,
            silent=True,
            importance_type='split'
        )
        clf.set_params(**{**opt_params, **self.params})
        return clf

    def modelXGBClassifier(self, trial: optuna.trial.Trial):
        opt_params = dict(
            max_depth=trial.suggest_int("max_depth", 2, 2 ** 4),
            learning_rate=trial.suggest_discrete_uniform('learning_rate', 0.001, 1, 0.001),
            n_estimators=trial.suggest_int("n_estimators", 2, 2 ** 10, log=True),
            gamma=trial.suggest_loguniform('gamma', 1e-8, 1),
            min_child_weight=trial.suggest_loguniform('min_child_weight', 1e-8, 2 ** 10),
            subsample=trial.suggest_uniform('subsample', 0.1, 1),
            colsample_bytree=trial.suggest_uniform('colsample_bytree', 0.1, 1),
            colsample_bylevel=trial.suggest_uniform('colsample_bylevel', 0.1, 1),
            reg_alpha=trial.suggest_loguniform('reg_alpha', 1e-8, 10),
            reg_lambda=trial.suggest_loguniform('reg_lambda', 1e-8, 10),
        )
        clf = XGBClassifier(
            max_depth=3,
            learning_rate=0.1,
            n_estimators=100,
            silent=True,
            objective="binary:logistic",
            booster='gbtree',
            n_jobs=1,
            gamma=0,
            min_child_weight=1,
            max_delta_step=0,
            subsample=1,
            colsample_bytree=1,
            colsample_bylevel=1,
            reg_alpha=0,
            reg_lambda=1,
            scale_pos_weight=1,
            base_score=0.5,
            random_state=0,
            missing=None
        )
        clf.set_params(**{**opt_params, **self.params})
        return clf

    def modelCatBoostClassifier(self, trial: optuna.trial.Trial):
        opt_params = dict(
            num_leaves=trial.suggest_int("num_leaves", 2, 2 ** 8),
            learning_rate=trial.suggest_discrete_uniform('learning_rate', 0.001, 1, 0.001),
            n_estimators=trial.suggest_int("n_estimators", 2, 2 ** 10, log=True),

            min_child_samples=trial.suggest_int('min_child_samples', 2, 2 ** 8),
            min_child_weight=trial.suggest_loguniform('min_child_weight', 1e-8, 1),
            min_split_gain=trial.suggest_loguniform('min_split_gain', 1e-8, 1),

            subsample=trial.suggest_uniform('subsample', 0.4, 1),
            subsample_freq=trial.suggest_int("subsample_freq", 0, 2 ** 4),
            colsample_bytree=trial.suggest_uniform('colsample_bytree', 0.4, 1),
            reg_alpha=trial.suggest_loguniform('reg_alpha', 1e-8, 10),
            reg_lambda=trial.suggest_loguniform('reg_lambda', 1e-8, 10),
        )
        clf = CatBoostClassifier()
        clf.set_params(**{**opt_params, **self.params})
        return clf

    def modelRandomForestClassifier(self, trial: optuna.trial.Trial):
        opt_params = dict(
            n_estimators=trial.suggest_int("n_estimators", 2, 2 ** 9, log=True),
            max_depth=trial.suggest_int("max_depth", 2, 2 ** 4),
            learning_rate=trial.suggest_discrete_uniform('learning_rate', 0.001, 1, 0.001),
            min_samples_leaf=trial.suggest_int("min_samples_leaf", 1, 10),

            criterion=trial.suggest_categorical("criterion", ["gini", "entropy"])
        )
        print(opt_params)

        clf = RandomForestClassifier(
            n_estimators=100,
            criterion="gini",
            max_depth=None,
            min_samples_split=2,
            min_samples_leaf=1,
            min_weight_fraction_leaf=0.,
            max_features="auto",
            max_leaf_nodes=None,
            min_impurity_decrease=0.,
            min_impurity_split=None,
            bootstrap=True,
            oob_score=False,
            n_jobs=-1,
            random_state=None,
            verbose=0,
            warm_start=False,
            class_weight=None,
            ccp_alpha=0.0,
            max_samples=None
        )

        clf.set_params(**{**opt_params, **self.params})
        return clf

    def modelBaggingClassifier(self, trial: optuna.trial.Trial):
        opt_params = dict(
            n_estimators=trial.suggest_int("n_estimators", 2, 2 ** 10, log=True),
            max_samples=trial.suggest_uniform('max_samples', 0.1, 1),
            learning_rate=trial.suggest_discrete_uniform('learning_rate', 0.001, 1, 0.001),
        )
        clf = BaggingClassifier(
            base_estimator=None,
            n_estimators=10,
            max_samples=1.0,
            max_features=1.0,
            bootstrap=True,
            bootstrap_features=False,
            oob_score=False,
            warm_start=False,
            n_jobs=-1,
            random_state=None,
            verbose=0
        )
        clf.set_params(**{**opt_params, **self.params})
        return clf

    def modelKNeighborsClassifier(self, trial: optuna.trial.Trial):
        opt_params = dict(
            n_neighbors=trial.suggest_int("n_neighbors", 2, 2 ** 5),
        )
        clf = KNeighborsClassifier(
            n_neighbors=5,
            weights='uniform',
            algorithm='auto',
            leaf_size=30,
            p=2,
            metric='minkowski',
            metric_params=None,
            n_jobs=-1)

        clf.set_params(**{**opt_params, **self.params})
        return clf

    def modelAdaBoostClassifier(self, trial: optuna.trial.Trial):
        opt_params = dict(
            n_estimators=trial.suggest_int("n_estimators", 2, 2 ** 10, log=True),
            learning_rate=trial.suggest_discrete_uniform('learning_rate', 0.001, 1, 0.001),

        )
        clf = AdaBoostClassifier(
            base_estimator=None,
            n_estimators=50,
            learning_rate=1.,
            algorithm='SAMME.R',
            random_state=None)

        clf.set_params(**{**opt_params, **self.params})
        return clf

    def modelExtraTreesClassifier(self, trial: optuna.trial.Trial):
        opt_params = dict(
            n_estimators=trial.suggest_int("n_estimators", 2, 2 ** 10, log=True),
            learning_rate=trial.suggest_discrete_uniform('learning_rate', 0.001, 1, 0.001),
            max_depth=trial.suggest_int("max_depth", 2, 2 ** 4),
            criterion=trial.suggest_categorical("criterion", ["gini", "entropy"])

        )
        clf = ExtraTreesClassifier(
            n_estimators=100,
            criterion="gini",
            max_depth=None,
            min_samples_split=2,
            min_samples_leaf=1,
            min_weight_fraction_leaf=0.,
            max_features="auto",
            max_leaf_nodes=None,
            min_impurity_decrease=0.,
            min_impurity_split=None,
            bootstrap=False,
            oob_score=False,
            n_jobs=None,
            random_state=None,
            verbose=0,
            warm_start=False,
            class_weight=None,
            ccp_alpha=0.0,
            max_samples=None
        )

        clf.set_params(**{**opt_params, **self.params})
        return clf

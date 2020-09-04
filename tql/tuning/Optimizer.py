#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tuning.
# @File         : Optimizer
# @Time         : 2020/9/2 1:32 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :
import json
import optuna
from optuna.samplers import TPESampler
from sklearn.model_selection import cross_val_score

from tql.tuning.ModelZoo import ModeZoo


class Optimizer(object):
    def __init__(self, X, y, model_obj=ModeZoo('LGBMClassifier', direction="maximize"), trials=1, cv=3):
        self.X = X
        self.y = y
        self.model_obj = model_obj
        self.direction = model_obj.direction
        self.trials = trials
        self.sampler = TPESampler(seed=777)
        self.cv = cv

    def run(self, gc_after_trial=False, show_progress_bar=False):
        self.study = optuna.create_study(direction=self.direction, sampler=self.sampler)
        self.study.optimize(
            self.__objective,
            n_trials=self.trials,
            gc_after_trial=gc_after_trial,
            show_progress_bar=show_progress_bar
        )
        print(f"best_params:\n{json.dumps(self.study.best_params, indent=4)}")

    def __objective(self, trial: optuna.trial.Trial):
        score = cross_val_score(self.model_obj(trial), self.X, self.y, n_jobs=1, cv=self.cv)
        return score.mean()


if __name__ == '__main__':
    from sklearn.datasets import load_iris

    iris = load_iris()
    X, y = iris.data[:100], iris.target[:100]
    opt = Optimizer(X, y)
    opt.run()

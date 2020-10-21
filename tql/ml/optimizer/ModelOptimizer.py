#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tuning.
# @File         : Optimizer
# @Time         : 2020/9/2 1:32 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :

# TODO: BaseOptimizer

import json
import optuna
from optuna.samplers import TPESampler
from sklearn.model_selection import cross_val_score

from tql.ml.optimizer.ModelZoo import ModelZoo


class ModelOptimizer(object):
    def __init__(self, X, y, model_obj=ModelZoo('LGBMClassifier', higher_is_better=True), cv=3):
        self.X = X
        self.y = y
        self.model_obj = model_obj
        self.direction = 'maximize' if model_obj.higher_is_better else 'minimize'
        self.cv = cv

    def run(self, trials=1, n_jobs=1, plot=True, gc_after_trial=False, seed=777):
        show_progress_bar = False if n_jobs > 1 else True

        self.study = optuna.create_study(direction=self.direction, sampler=TPESampler(seed=seed))
        self.study.optimize(
            self.__objective,
            n_trials=trials,
            gc_after_trial=gc_after_trial,
            show_progress_bar=show_progress_bar,
            n_jobs=n_jobs
        )

        if plot:
            print(f"best_params:\n{json.dumps(self.study.best_params, indent=4)}")
            self._plot()

    def __objective(self, trial: optuna.trial.Trial):
        score = cross_val_score(self.model_obj(trial), self.X, self.y, n_jobs=1, cv=self.cv)
        return score.mean()

    def _plot(self):
        # optuna.visualization.plot_slice(self.study)
        _ = optuna.visualization.plot_optimization_history(self.study)
        return _


if __name__ == '__main__':
    from sklearn.datasets import load_iris

    iris = load_iris()
    X, y = iris.data[:100], iris.target[:100]
    opt = ModelOptimizer(X, y)
    opt.run()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : F1Optimizer
# @Time         : 2020/9/21 10:11 上午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

import optuna
import numpy as np

from sklearn.metrics import f1_score
from tql.ml.optimizer.BaseOptimizer import BaseOptimizer


class F1Optimizer(BaseOptimizer):

    def __init__(self, y_true, y_pred):
        self.y_true = np.array(y_true)
        self.y_pred = np.array(y_pred)

    def _objective(self, trial: optuna.trial.Trial):
        threshold = trial.suggest_discrete_uniform('threshold', 0.001, 1, 0.001)
        y_pred_ = np.where(self.y_pred > threshold, 1, 0)
        score = f1_score(self.y_true, y_pred_)
        return score


if __name__ == '__main__':
    F1Optimizer([1, 1, 0, 0], [0.1, 0.2, 0.3, 0.4]).run()

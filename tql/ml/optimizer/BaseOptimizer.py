#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : BaseOptimizer
# @Time         : 2020/9/21 12:53 上午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :
import abc
import json
import joblib
import optuna
from optuna.samplers import TPESampler

optuna.logging.set_verbosity(optuna.logging.ERROR)


class BaseOptimizer(object):

    @abc.abstractmethod
    def _objective(self, trial: optuna.trial.Trial):
        raise NotImplementedError("overwrite objective!!!")

    def run(self, trials=3, n_jobs=1, plot=True, gc_after_trial=False, seed=777):
        show_progress_bar = False if n_jobs > 1 else True

        self.study = optuna.create_study(direction='maximize', sampler=TPESampler(seed=seed))
        self.study.optimize(
            self._objective,
            n_trials=trials,
            gc_after_trial=gc_after_trial,
            show_progress_bar=show_progress_bar,
            n_jobs=n_jobs
        )

        if plot:
            print(f"best_params:\n{json.dumps(self.study.best_params, indent=4)}")
            return self._plot()

    def trials_dataframe(self):
        df_trials = self.study.trials_dataframe().sort_values('value', ascending=False)

        return df_trials

    def top_params(self, topK=5, save_file=None):
        params_dict = (
            self.trials_dataframe().iloc[:topK, :]
                .filter(like='params_')
                .rename(columns=lambda col: col.split('params_')[1])
                .to_dict('records')
        )
        if save_file is not None:
            with open(save_file, 'w') as f:
                print(params_dict, file=f)

        return params_dict

    def _plot(self):
        # optuna.visualization.plot_slice(self.study)
        _ = optuna.visualization.plot_optimization_history(self.study)

        # optuna.visualization.plot_param_importances(self.study)
        # optuna.visualization.plot_edf(self.study)
        # optuna.visualization.plot_parallel_coordinate(self.study)
        return _


if __name__ == '__main__':
    import numpy as np

    from sklearn.metrics import f1_score


    class SimpleOptimizer(BaseOptimizer):

        def __init__(self, y_true, y_pred):
            self.y_true = np.array(y_true)
            self.y_pred = np.array(y_pred)

        def _objective(self, trial: optuna.trial.Trial):
            threshold = trial.suggest_discrete_uniform('threshold', 0.001, 1, 0.001)
            y_pred_ = np.where(self.y_pred > threshold, 1, 0)
            score = f1_score(self.y_true, y_pred_)
            return score


    SimpleOptimizer([1, 1, 0, 0], [0.1, 0.2, 0.3, 0.4]).run()

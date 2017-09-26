from scipy.stats import halfnorm, randint as sp_randint, uniform
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.model_selection import StratifiedKFold
from typing import List, Tuple, Type, Union
import itertools
import numpy as np
import os
import xgboost as xgb


def clean_params_for_sk(params: dict) -> dict:
    """
    Given a dictionary of XGB parameters, return a copy without parameters that will cause issues with scikit-learn's grid or
    randomized search estimators.

    :param params:
        A dictionary of XGB parameters.
    :return:
        A copy of the same dictionary without the aforementioned problematic parameters.
    """
    # In the xgb.cv call, nthread should be equal to the CPU count, but this causes a hang when
    # called through GridSearchCV - parallelism should be achieved through its n_jobs parameter.
    # See https://github.com/scikit-learn/scikit-learn/issues/6627 for more details.
    params_copy = params.copy()
    params_copy['nthread'] = 1

    # In multiclass problems, this parameter is required for XGBoost, but is not a parameter of interest to be tuned.
    if 'num_class' in params_copy.keys():
        del params_copy['num_class']

    return params_copy


def tune_num_estimators(metric: str,
                        label: np.ndarray,
                        params: dict,
                        strat_folds: StratifiedKFold,
                        train) -> Tuple[int, float]:
    """
    Uses xgboost's cross-validation method to tune the number of estimators and returns that along with the best CV score
    achieved.

    :param metric:
        Evaluation metric that is monitored during cross-validation - e.g. 'logloss' or 'rmse'.
    :param label:
        An array-like containing the labels of the classification or regression problem.
    :param params:
        A dictionary of XGB parameters.
    :param strat_folds:
        A StratifiedKFold object to cross validate the parameters.
    :param train:
        An array-like containing the training input samples.
    :return:
        A tuple containing the tuned number of estimators along with the best CV score achieved.
    """
    eval_hist = xgb.cv(
        dtrain=xgb.DMatrix(train, label=label),
        early_stopping_rounds=50,
        folds=strat_folds,
        metrics=metric,
        num_boost_round=10000,
        params=params,
        verbose_eval=True
    )
    num_trees = eval_hist.shape[0]
    best_score = eval_hist.values[num_trees - 1, 0]
    return num_trees, best_score


def tune_xgb_params_segment_by_grid(estimator_cls: Type[Union[xgb.XGBClassifier, xgb.XGBRegressor]],
                                    label: np.ndarray,
                                    metric_sklearn: str,
                                    n_jobs: int,
                                    param_grid: dict,
                                    params: dict,
                                    strat_folds: StratifiedKFold,
                                    train: np.ndarray,
                                    verbosity_level: int = 10) -> Tuple[dict, float]:
    """
    Grid search over a segment of XGBoost parameters.

    :param estimator_cls:
        The class type of the estimator to instantiate - either an XGBClassifier or an XGBRegressor.
    :param label:
        An array-like containing the labels of the classification or regression problem.
    :param metric_sklearn:
        The evaluation metric to be passed to scikit-learn's GridSearchCV - see
        http://scikit-learn.org/stable/modules/model_evaluation.html
        for the options this can take - e.g. 'neg_mean_squared_error' for RMSE.
    :param n_jobs:
        The number of jobs to run simultaneously.
    :param param_grid:
        A dictionary of the grid of parameters to be searched over - e.g. {'colsample_bytree': range(0.5, 0.9, 0.1)} to search
        values [0.5, 0.6, 0.7, 0.8].
    :param params:
        A dictionary of XGB parameters.
    :param strat_folds:
        A StratifiedKFold object to cross validate the parameters.
    :param train:
        An array-like containing the training input samples.
    :param verbosity_level:
        An optional parameter to control the verbosity of the grid searching - defaults to the most verbose option.
    :return:
        A dictionary of tuned parameters and a list of the parameters found at each step with their respective scores.
    """
    params_copy = clean_params_for_sk(params)

    grid = GridSearchCV(
        cv=strat_folds.split(train, label),
        estimator=estimator_cls(**params_copy),
        n_jobs=n_jobs,
        param_grid=param_grid,
        scoring=metric_sklearn,
        verbose=verbosity_level
    )
    grid.fit(train, label)
    best_score = grid.best_score_
    # Massage the score to be in line with what xgboost reports
    if metric_sklearn == 'neg_mean_squared_error':
        best_score = abs(best_score) ** 0.5
    elif metric_sklearn == 'neg_log_loss':
        best_score = abs(best_score)
    return {k: grid.best_params_[k] for k in param_grid.keys()}, best_score


def tune_xgb_params_randomized(estimator_cls,
                               label: np.ndarray,
                               metric_sklearn: str,
                               n_jobs: int,
                               params: dict,
                               strat_folds: StratifiedKFold,
                               train: np.ndarray,
                               n_iter: int = 20,
                               verbosity_level: int = 10,
                               **kwargs):
    """
    :param estimator_cls:
        The class type of the estimator to instantiate - either an XGBClassifier or an XGBRegressor.
    :param label:
        An array-like containing the labels of the classification or regression problem.
    :param metric_sklearn:
        The evaluation metric to be passed to scikit-learn's GridSearchCV - see
        http://scikit-learn.org/stable/modules/model_evaluation.html
        for the options this can take - e.g. 'neg_mean_squared_error' for RMSE.
    :param n_jobs:
        The number of jobs to run simultaneously.
    :param params:
        A dictionary of XGB parameters.
    :param strat_folds:
        A StratifiedKFold object to cross validate the parameters.
    :param train:
        An array-like containing the training input samples.
    :param n_iter:
        An optional parameter to control the number of parameter settings that are sampled.
    :param n_jobs:
        An optional parameter to control the amount of parallel jobs - defaults to the amount of CPUs available.
    :param verbosity_level:
        An optional parameter to control the verbosity of the grid searching - defaults to the most verbose option.
    :param kwargs:
        Parameter distributions may be controlled through keyword arguments - e.g. to sample uniformly between 0.5 and 0.7 for
        colsample_bytree, supply colsample_bytree_loc=0.5 and colsample_bytree_scale=0.2.
    :return:
        A dictionary of tuned parameters and a list of the parameters found at each step with their respective scores.
    """
    params_copy = clean_params_for_sk(params)
    param_distributions = {
        'colsample_bytree': uniform(kwargs.get('colsample_bytree_loc', 0.2), kwargs.get('colsample_bytree_scale', 0.8)),
        'gamma': uniform(kwargs.get('gamma_loc', 0), kwargs.get('gamma_scale', 0.9)),
        'max_depth': sp_randint(kwargs.get('max_depth_low', 6), kwargs.get('max_depth_high', 11)),
        'min_child_weight': sp_randint(kwargs.get('min_child_weight_low', 1), kwargs.get('min_child_weight_high', 11)),
        'reg_alpha': halfnorm(kwargs.get('reg_alpha_loc', 0), kwargs.get('reg_alpha_scale', 5)),
        'reg_lambda': halfnorm(kwargs.get('reg_alpha_loc', 0), kwargs.get('reg_alpha_scale', 5)),
        'subsample': uniform(kwargs.get('subsample_loc', 0.2), kwargs.get('subsample_scale', 0.8))
    }

    rand_search = RandomizedSearchCV(
        cv=strat_folds.split(train, label),
        estimator=estimator_cls(**params_copy),
        n_iter=n_iter,
        n_jobs=n_jobs,
        param_distributions=param_distributions,
        scoring=metric_sklearn,
        verbose=verbosity_level
    )
    rand_search.fit(train, label)
    return rand_search.best_params_, [(rand_search.best_params_, rand_search.best_score_)]


def tune_xgb_params_incremental(estimator_cls,
                                label: np.ndarray,
                                metric_sklearn: str,
                                n_jobs: int,
                                params: dict,
                                strat_folds: StratifiedKFold,
                                train: np.ndarray,
                                colsample_bytree_max: float = 1.0,
                                colsample_bytree_min: float = 0.6,
                                colsample_bytree_step: float = 0.1,
                                gamma_max: float = 0.5,
                                gamma_min: float = 0.0,
                                gamma_step: float = 0.1,
                                max_depth_step: int = 1,
                                max_depth_min: int = 3,
                                max_depth_max: int = 10,
                                min_child_weight_max: int = 6,
                                min_child_weight_min: int = 1,
                                min_child_weight_step: int = 1,
                                subsample_max: float = 1.0,
                                subsample_min: float = 0.6,
                                subsample_step: float = 0.1,
                                **kwargs) -> Tuple[dict, List[Tuple[dict, float]]]:
    """
    Tunes XGB parameters incrementally as suggested on
    https://www.analyticsvidhya.com/blog/2016/03/complete-guide-parameter-tuning-xgboost-with-codes-python/

    :param estimator_cls:
        The class type of the estimator to instantiate - either an XGBClassifier or an XGBRegressor.
    :param label:
        An array-like containing the labels of the classification or regression problem.
    :param metric_sklearn:
        The evaluation metric to be passed to scikit-learn's GridSearchCV - see
        http://scikit-learn.org/stable/modules/model_evaluation.html
        for the options this can take - e.g. 'neg_mean_squared_error' for RMSE.
    :param n_jobs:
        The number of jobs to run simultaneously.
    :param params:
        A dictionary of XGB parameters.
    :param strat_folds:
        A StratifiedKFold object to cross validate the parameters.
    :param train:
        An array-like containing the training input samples.
    :param colsample_bytree_max:
        The maximum (inclusive) value to try for the colsample_bytree XGBoost parameter.
    :param colsample_bytree_min:
        The minimum (inclusive) value to try for the colsample_bytree XGBoost parameter.
    :param colsample_bytree_step:
        The step between values to try for the colsample_bytree XGBoost parameter.
    :param gamma_max:
        The maximum (inclusive) value to try for the gamma XGBoost parameter.
    :param gamma_min:
        The minimum (inclusive) value to try for the gamma XGBoost parameter.
    :param gamma_step:
        The step between values to try for the gamma XGBoost parameter.
    :param max_depth_max:
        The maximum (inclusive) value to try for the max_depth XGBoost parameter.
    :param max_depth_min:
        The minimum (inclusive) value to try for the max_depth XGBoost parameter.
    :param max_depth_step:
        The step between values to try for the max_depth XGBoost parameter.
    :param min_child_weight_max:
        The maximum (inclusive) value to try for the min_child_weight XGBoost parameter.
    :param min_child_weight_min:
        The minimum (inclusive) value to try for the min_child_weight XGBoost parameter.
    :param min_child_weight_step:
        The step between values to try for the min_child_weight XGBoost parameter.
    :param subsample_max:
        The maximum (inclusive) value to try for the subsample XGBoost parameter.
    :param subsample_min:
        The minimum (inclusive) value to try for the subsample XGBoost parameter.
    :param subsample_step:
        The step between values to try for the subsample XGBoost parameter.
    :return:
        A dictionary of tuned parameters and a list of the parameters found at each step with their respective scores.
    """
    params_copy = clean_params_for_sk(params)
    history = []

    param_grids = [
        {
            'max_depth': range(max_depth_min, max_depth_max + 1, max_depth_step),
            'min_child_weight': range(min_child_weight_min, min_child_weight_max + 1, min_child_weight_step)
        },
        {
            'gamma': np.linspace(
                gamma_min,
                gamma_max,
                round((gamma_max - gamma_min) / gamma_step) + 1
            )
        },
        {
            'colsample_bytree': np.linspace(
                colsample_bytree_min,
                colsample_bytree_max,
                round((colsample_bytree_max - colsample_bytree_min) / colsample_bytree_step) + 1
            ),
            'subsample': np.linspace(
                subsample_min,
                subsample_max,
                round((subsample_max - subsample_min) / subsample_step) + 1
            )
        },
        {'reg_alpha': list(itertools.chain([0], [10 ** i for i in range(-6, 3)], [(10 ** i) / 2 for i in range(-6, 3)]))},
        {'reg_lambda': list(itertools.chain([0], [10 ** i for i in range(-6, 3)], [(10 ** i) / 2 for i in range(-6, 3)]))}
    ]
    for param_grid in param_grids:
        new_params, score = tune_xgb_params_segment_by_grid(
            estimator_cls=estimator_cls,
            label=label,
            metric_sklearn=metric_sklearn,
            n_jobs=n_jobs,
            param_grid=param_grid,
            params=params_copy,
            strat_folds=strat_folds,
            train=train,
            **kwargs
        )
        history.append((params_copy.copy(), score))
        # Don't overwrite parameters that were removed or changed for sklearn
        params_copy.update({k: new_params[k] for k in param_grid.keys()})

    return params_copy, history


def tune_xgb_params(label: np.ndarray,
                    metric_sklearn: str,
                    metric_xgb: str,
                    objective: str,
                    strategy: str,
                    train: np.ndarray,
                    cv_folds: int = 5,
                    init_colsample_bytree: float = 0.8,
                    init_gamma: float = 0,
                    init_learning_rate: float = 0.1,
                    init_max_depth: int = 6,
                    init_min_child_weight: int = 1,
                    init_subsample: float = 0.8,
                    lower_learning_rate: float = 0.01,
                    n_jobs: int = None,
                    seed: int = None,
                    **kwargs) -> Tuple[dict, List[Tuple[dict, float]]]:
    """
    :param label:
        An array-like containing the labels of the classification or regression problem.
    :param metric_sklearn:
        The evaluation metric to be passed to scikit-learn's GridSearchCV - see
        http://scikit-learn.org/stable/modules/model_evaluation.html
        for the options this can take - e.g. 'neg_mean_squared_error' for RMSE.
    :param metric_xgb:
        The evaluation metric to be passed to xgb.cv - see
        http://xgboost.readthedocs.io/en/latest/parameter.html
        for the options this can take - e.g. 'rmse' for RMSE.
    :param objective:
        An XGB objective - e.g. 'binary:logistic' or 'reg:linear'.
    :param strategy:
        A string that must be either 'incremental' or 'randomized' to indicate how to tune the parameters.
    :param train:
        An array-like containing the training input samples.
    :param cv_folds:
        The number of cross-validation folds - defaults to 5.
    :param init_colsample_bytree:
        The initial colsample_bytree parameter for XGB.
    :param init_gamma:
        The initial gamma parameter for XGB.
    :param init_learning_rate:
        The initial learning rate parameter for XGB.
    :param init_max_depth:
        The initial maximum depth parameter for XGB.
    :param init_min_child_weight:
        The initial minimum child weight parameter for XGB.
    :param init_subsample:
        The initial subsample parameter for XGB.
    :param lower_learning_rate:
        A lower learning rate (which must be lower than the initial learning rate) to try with the tuned parameters after they
        have been selected.
    :param n_jobs:
        An optional parameter to control the amount of parallel jobs - defaults to the amount of CPUs available.
    :param seed:
        An optional random seed for reproducibility of results.
    :param kwargs:
        Parameter tuning distributions or ranges may be specified through kwargs. If not, sensible options are chosen.
    :return:
        A dictionary of tuned parameters and a list of the parameters found at each step with their respective scores.
    """
    assert lower_learning_rate < init_learning_rate, 'Final learning rate should be lower than the initial rate.'
    assert strategy in ['incremental', 'randomized'], 'Tuning strategy must be in {incremental, randomized}.'
    cur_xgb_params = {
        'colsample_bytree': init_colsample_bytree,
        'gamma': init_gamma,
        'learning_rate': init_learning_rate,
        'max_depth': init_max_depth,
        'min_child_weight': init_min_child_weight,
        'nthread': n_jobs or os.cpu_count(),
        'objective': objective,
        'scale_pos_weight': 5,                            # 负/正样本比
        'subsample': init_subsample
    }
    estimator_cls_map = {
        'binary': xgb.XGBClassifier,
        'count': xgb.XGBRegressor,
        'multi': xgb.XGBClassifier,
        'rank': xgb.XGBRegressor,
        'reg': xgb.XGBRegressor
    }
    estimator_cls = estimator_cls_map[objective.split(':')[0]]

    # For multi-objective problems, the # of unique classes must be set in the parameters.
    is_multi_class = objective.startswith('multi')
    if is_multi_class:
        cur_xgb_params['num_class'] = len(label.unique())
    if seed is not None:
        cur_xgb_params['seed'] = seed

    strat_folds = StratifiedKFold(n_splits=cv_folds, random_state=seed)
    init_num_estimators, init_score = tune_num_estimators(
        metric=metric_xgb,
        label=label,
        params=cur_xgb_params,
        strat_folds=strat_folds,
        train=train
    )
    cur_xgb_params['n_estimators'] = init_num_estimators
    history = [(cur_xgb_params.copy(), init_score)]

    # Set the random state if specified for reproducibility
    np.random.seed(seed)

    if strategy == 'incremental':
        new_params, tune_history = tune_xgb_params_incremental(
            estimator_cls=estimator_cls,
            label=label,
            metric_sklearn=metric_sklearn,
            n_jobs=n_jobs,
            params=cur_xgb_params,
            strat_folds=strat_folds,
            train=train,
            **kwargs
        )
    else:
        new_params, tune_history = tune_xgb_params_randomized(
            estimator_cls=estimator_cls,
            label=label,
            metric_sklearn=metric_sklearn,
            n_jobs=n_jobs,
            params=cur_xgb_params,
            strat_folds=strat_folds,
            train=train,
            **kwargs
        )
    cur_xgb_params.update({k: v for k, v in new_params.items() if k not in {'nthread', 'num_classes'}})
    history.extend(tune_history)

    # Lower the learning rate and find the optimal number of estimators
    cur_xgb_params['learning_rate'] = lower_learning_rate
    cur_xgb_params['n_estimators'], lower_rate_score = tune_num_estimators(
        label=label,
        metric=metric_xgb,
        params=cur_xgb_params,
        strat_folds=strat_folds,
        train=train
    )
    history.append((cur_xgb_params.copy(), lower_rate_score))

    # Select the old learning rate based on the new score, but the ordering of what's better depends on the objective.
    is_init_superior = (metric_xgb == 'auc' and init_score > lower_rate_score)
    is_init_superior |= (metric_xgb != 'auc' and init_score < lower_rate_score)
    if is_init_superior:
        cur_xgb_params['learning_rate'] = init_learning_rate
        cur_xgb_params['n_estimators'] = init_num_estimators

    # In multiclass problems, this parameter is required for XGBoost, but is not a parameter of interest to be tuned.
    if is_multi_class:
        del cur_xgb_params['num_class']

    return cur_xgb_params, history

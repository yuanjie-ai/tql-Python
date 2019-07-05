#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'tpot'
__author__ = 'JieYuan'
__mtime__ = '19-1-3'
"""

from tpot import TPOTRegressor

TPOTRegressor(
    generations=100,
    population_size=100,
    offspring_size=None,
    mutation_rate=0.9,
    crossover_rate=0.1,
    scoring=None,
    cv=5,
    subsample=1.0,
    n_jobs=1,
    max_time_mins=None,
    max_eval_time_mins=5,
    random_state=None,
    config_dict=None,
    warm_start=False,
    memory=None,
    use_dask=False,
    periodic_checkpoint_folder=None,
    early_stop=None,
    verbosity=0,
    disable_update_check=False)

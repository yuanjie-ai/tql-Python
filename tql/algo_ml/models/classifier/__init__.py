#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '__init__.py'
__author__ = 'JieYuan'
__mtime__ = '19-1-2'
"""

from .baseline_lgb import BaselineLGB
from .baseline_xgb import BaselineXGB
from .bayes_opt_lgb import BayesOptLGB
from .bayes_opt_xgb import BayesOptXGB

# _clf = LGBMClassifier(n_estimators=1)
# X = iris.data[:100, :]
# y = iris.target[:100]
# _clf.fit(X, y)
# show_info = ['split_gain', 'internal_value', 'internal_count', 'leaf_count']
# lgb.plot_tree(_clf.booster_, figsize=(60, 80), show_info=show_info)
#
# model = _clf.booster_.dump_model()
# tree_infos = model['tree_info'] # xgb_._Booster.get_dump()
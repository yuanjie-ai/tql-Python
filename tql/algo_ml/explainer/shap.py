#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'shap'
__author__ = 'JieYuan'
__mtime__ = '2019-05-09'
"""
# import xgboost
# import shap
#
# # load JS visualization code to notebook
# shap.initjs()
#
# # train XGBoost model
# X, y = shap.datasets.boston()
# model = xgboost.train({"learning_rate": 0.01}, xgboost.DMatrix(X, label=y), 100)
#
# # explain the model's predictions using SHAP values
# # (same syntax works for LightGBM, CatBoost, and scikit-learn models)
# explainer = shap.TreeExplainer(model)
#
# _X = X.iloc[0, :]
# shap_values = explainer.shap_values(_X)
# # visualize the first prediction's explanation (use matplotlib=True to avoid Javascript)
# shap.force_plot(explainer.expected_value, shap_values, _X)

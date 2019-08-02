#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'get_label'
__author__ = 'JieYuan'
__mtime__ = '19-1-28'
"""
import numpy as np
import pandas as pd


def get_threshold_or_label(preds, psr, only_return_threshold=False):
    """默认: 指标>阈值为正样本
    :param psr: Positive sample ratio
    :return:
    """
    threshold = pd.Series(preds).quantile(1 - psr)
    if only_return_threshold:
        return threshold
    else:
        return np.where(preds > threshold, 1, 0)

# def threshold_search(y_true, y_proba):
#     best_threshold = 0
#     best_score = 0
#     for threshold in tqdm([i * 0.01 for i in range(100)]):
#         score = f1_score(y_true=y_true, y_pred=y_proba > threshold)
#         if score > best_score:
#             best_threshold = threshold
#             best_score = score
#     search_result = {'threshold': best_threshold, 'f1': best_score}
#     return search_result

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'feval'
__author__ = 'JieYuan'
__mtime__ = '19-3-18'
"""
import wrapt

def feval(multiclass=None, is_bigger_better=True, model='lgb'):
    """example
    @feval(3)
    def f1_score(y_pred, y_true):
        '注意入参顺序'
        return f1_score(y_true, y_pred, average='macro')
    """

    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        y_pred, y_true = args
        y_true = y_true.get_label()
        if model == 'lgb':
            if multiclass:
                y_pred = np.array(y_pred).reshape(multiclass, -1).argmax(0)
            return wrapped.__name__, wrapped(y_pred, y_true), is_bigger_better
        elif is_bigger_better:
            """xgb评估指标默认越小越好"""
            return '-' + wrapped.__name__, - wrapped(y_pred, y_true)
        else:
            return wrapped.__name__, wrapped(y_pred, y_true)

    return wrapper

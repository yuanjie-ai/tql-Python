#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : SupervisedSampling
# @Time         : 2020/9/24 12:14 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

import numpy as np


class SupervisedSampling(object):
    """根据pred淘汰掉部分正负样本"""

    def keep_samples(self, X, y, y_pred, confidence=0.001, drop_pos_sample=False):
        """

        :param confidence: 剔除低于分位数的样本或者样本数
        """
        assert len(y_pred) == len(y) == len(X)

        if confidence > 1:
            confidence = confidence / len(X)
        threshold = np.quantile(y_pred, confidence)

        keep_index = np.where(y_pred > threshold)[0]
        if not drop_pos_sample:
            pos_index = np.where(y == 1)[0]
            keep_index = list(set(keep_index) | set(pos_index)) # 并集

        # 剔除数据
        print(f"Drop num_sample={len(X)-len(keep_index)}")
        return X[keep_index], y[keep_index]

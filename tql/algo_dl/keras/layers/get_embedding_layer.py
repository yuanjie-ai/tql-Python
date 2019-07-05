#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-cloudml.
# @File         : get_embedding_layer
# @Time         : 2019-06-21 16:25
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :
from tensorflow.python.keras.layers import Embedding

def get_keras_embedding(maxlen, weights=None, trainable=False):
    """

    :param maxlen: 输入序列的长度，当它是固定的时。如果你需要连接 Flatten 和 Dense层，则这个参数是必须的（没有它，dense层的输出尺寸就无法计算）
    :param weights: vectors
    :param trainable:
    :return:
    """
    m, n = weights.shape  # 词数/类别数 * 输出向量维度
    layer = Embedding(input_dim=m,
                      output_dim=n,
                      weights=[weights] if weights else None,
                      trainable=trainable,
                      input_length=maxlen)

    return layer

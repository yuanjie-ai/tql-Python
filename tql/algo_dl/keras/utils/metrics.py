#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : metrics
# @Time         : 2019-07-03 17:10
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

import tensorflow as tf
import tensorflow.python.keras.backend as K
tf.keras.metrics.Accuracy()

# 参考losses.py编写自己的损失函数
# Retinanet 针对正负样本不均衡问题设计的损失函数focal_loss
# Keras 以tf为后端；可以使用Keras的math方法或者tf的math方法写都可以keras被识别
def focal_loss(y_true, y_pred, gamma=2., alpha=.25):
    pt_1 = tf.where(tf.equal(y_true, 1), y_pred, tf.ones_like(y_pred))
    pt_0 = tf.where(tf.equal(y_true, 0), y_pred, tf.zeros_like(y_pred))
    return K.mean(-alpha * K.pow(1 - pt_1, gamma) * K.log(pt_1) - (1 - alpha) * K.pow(pt_0, gamma) * K.log(1 - pt_0),
                  axis=-1)

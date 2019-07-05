#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : losses
# @Time         : 2019-07-03 17:15
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


import tensorflow as tf
from tensorflow.python.keras import backend as K


# 参考losses.py编写自己的损失函数
# Retinanet 针对正负样本不均衡问题设计的损失函数focal_loss
# Keras 以tf为后端；可以使用Keras的math方法或者tf的math方法写都可以keras被识别
def focal_loss(y_true, y_pred, gamma=2., alpha=.25):
    pt_1 = tf.where(tf.equal(y_true, 1), y_pred, tf.ones_like(y_pred))
    pt_0 = tf.where(tf.equal(y_true, 0), y_pred, tf.zeros_like(y_pred))
    return K.mean(-alpha * K.pow(1 - pt_1, gamma) * K.log(pt_1) - (1 - alpha) * K.pow(pt_0, gamma) * K.log(1 - pt_0),
                  axis=-1)

    # return -K.mean(alpha * K.pow(1. - pt_1, gamma) * K.log(pt_1)) - K.mean(
    #     (1 - alpha) * K.pow(pt_0, gamma) * K.log(1. - pt_0))


# return -K.sum(alpha * K.pow(1. - pt_1, gamma) * K.log(K.epsilon() + pt_1)) - K.sum(
#     (1 - alpha) * K.pow(pt_0, gamma) * K.log(1. - pt_0 + K.epsilon()))

# https://github.com/umbertogriffo/focal-loss-keras/blob/master/losses.py
# Define our custom loss function
def focal_loss(y_true, y_pred):
    gamma = 2.0
    alpha = 0.25
    pt_1 = tf.where(tf.equal(y_true, 1), y_pred, tf.ones_like(y_pred))
    pt_0 = tf.where(tf.equal(y_true, 0), y_pred, tf.zeros_like(y_pred))
    return - K.sum(alpha * K.pow(1. - pt_1, gamma) * K.log(pt_1)) - K.sum(
        (1 - alpha) * K.pow(pt_0, gamma) * K.log(1. - pt_0))


# 未调试
def catergorical_focal_loss(gamma=2.0, alpha=0.25):
    """
    Implementation of Focal Loss from the paper in multiclass classification
    Formula:
        loss = -alpha*((1-p_t)^gamma)*log(p_t)
    Parameters:
        alpha -- the same as wighting factor in balanced cross entropy
        gamma -- focusing parameter for modulating factor (1-p)
    Default value:
        gamma -- 2.0 as mentioned in the paper
        alpha -- 0.25 as mentioned in the paper
    """

    def focal_loss(y_true, y_pred):
        # Define epsilon so that the backpropagation will no result in NaN
        # for o divisor case
        epsilon = K.epsilon()
        # Add the epsilon to prediction value
        # y_pred = y_pred + epsilon
        # Clip the prediction value
        y_pred = K.clip(y_pred, epsilon, 1.0 - epsilon)
        # Calculate cross entropy
        cross_entropy = -y_true * K.log(y_pred)

        # Calculate weight that consists of modulating factor and weighting factor
        weight = alpha * y_true * K.pow((1 - y_pred), gamma)
        # Calculate focal loss
        loss = weight * cross_entropy
        # Sum the losses in mini_batch
        loss = K.sum(loss, axis=1)
        return loss

    return focal_loss


def binary_focal_loss(gamma=2.0, alpha=0.25):
    """
        Implementation of Focal Loss from the paper in multiclass classification
        Formula:
            loss = -alpha_t*((1-p_t)^gamma)*log(p_t)

            p_t = y_pred, if y_true = 1
            p_t = 1-y_pred, otherwise

            alpha_t = alpha, if y_true=1
            alpha_t = 1-alpha, otherwise

            cross_entropy = -log(p_t)
        Parameters:
            alpha -- the same as wighting factor in balanced cross entropy
            gamma -- focusing parameter for modulating factor (1-p)
        Default value:
            gamma -- 2.0 as mentioned in the paper
            alpha -- 0.25 as mentioned in the paper
        """

    def focal_loss(y_true, y_pred):
        # Define espislon so that the backpropagation will not result int NaN
        # for 0 divisor case
        epsilon = K.epsilon()
        # Add the epsilon to prediction value
        # y_pred = y_pred + epsilon
        # Clip the prediction value
        y_pred = K.clip(y_pred, epsilon, 1.0 - epsilon)

        alpha_factor = K.ones_like(y_true) * alpha

        # Calculate p_t
        p_t = tf.where(K.equal(y_true, 1), alpha_factor, 1 - alpha_factor)

        # Calculate alpha_t
        alpha_t = tf.where(K.equal(y_true, 1), alpha_factor, 1 - alpha_factor)
        # Calculate cross entropy
        cross_entropy = -K.log(p_t)
        weight = alpha_t * K.pow((1 - p_t), gamma)
        # Calculate focal loss
        loss = weight * cross_entropy
        # Sum the losses in mini_batch
        loss = K.sum(loss, axis=1)

        return loss

    return focal_loss

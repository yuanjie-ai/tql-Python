#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : inn.
# @File         : muit_inputs_outputs
# @Time         : 2020/5/18 9:31 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :


import tensorflow as tf
from tensorflow.keras.layers import *
from sklearn.datasets import load_iris

from inn.layers import DNN
from inn.dateset import Dataset

X, y = load_iris(True)
# 构建数据集
ds = Dataset().from_cache((X, X), (y, y))
# ds_test = Dataset().from_cache((X, X))

# 搭建模型
input1 = Input((4,))
input2 = Input((4,))
x = tf.keras.layers.concatenate([input1, input2])
x = DNN([64, 16, 4])(x)
output1 = Dense(1, 'sigmoid', name='fc1')(x)
output2 = Dense(1, 'sigmoid', name='fc2')(x)

model = tf.keras.Model(inputs=[input1, input2], outputs=[output1, output2])

# 目标函数定义，需与输出层名字对应
losses = {'fc1': 'categorical_crossentropy',
          'fc2': 'categorical_crossentropy'}

loss_weights = {'fc1': 0.9,
                'fc2': 0.1}

model.compile(loss=losses, loss_weights=loss_weights, metrics=['accuracy'])

model.fit(ds, epochs=1)  # model.fit(ds, epochs=1, steps_per_epoch=100)
# print(model.predict(ds_test))

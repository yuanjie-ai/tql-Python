#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : FM
# @Time         : 2019-07-16 16:12
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


"""
https://github.com/jfpuget/LibFM_in_Keras/blob/master/keras_blog.ipynb
Trick:
1. 单模型
2. 提取embedding共享特征与原特征拼接 + 其他基模型
"""
from tensorflow.python.keras import backend as K
from tensorflow.python.keras.models import Model
from tensorflow.python.keras.layers.normalization import BatchNormalization
from tensorflow.python.keras.layers import Input, Embedding, Dense, Flatten, Concatenate, Dot, Reshape, Add, Subtract
from tensorflow.python.keras.optimizers import Adam
from tensorflow.python.keras.regularizers import l2
from tensorflow.python.keras.callbacks import EarlyStopping, ModelCheckpoint

k_latent = 2
embedding_reg = 0.0002
kernel_reg = 0.1


def get_embed(x_input, x_size, k_latent):
    if x_size > 0:  # category
        embed = Embedding(x_size, k_latent, input_length=1,
                          embeddings_regularizer=l2(embedding_reg))(x_input)
        embed = Flatten()(embed)
    else:
        embed = Dense(k_latent, kernel_regularizer=l2(embedding_reg))(x_input)
    return embed


def build_model_1(f_size):
    dim_input = len(f_size)

    input_x = [Input(shape=(1,)) for i in range(dim_input)]
    biases = [get_embed(x, size, 1) for (x, size) in zip(input_x, f_size)]
    factors = [get_embed(x, size, k_latent) for (x, size) in zip(input_x, f_size)]

    s = Add()(factors)
    diffs = [Subtract()([s, x]) for x in factors]
    dots = [Dot(axes=1)([d, x]) for d, x in zip(diffs, factors)]

    x = Concatenate()(biases + dots)
    x = BatchNormalization()(x)
    output = Dense(1, activation='relu', kernel_regularizer=l2(kernel_reg))(x)
    model = Model(inputs=input_x, outputs=[output])
    model.compile(optimizer=Adam(clipnorm=0.5), loss='mean_squared_error')
    output_f = factors + biases
    model_features = Model(inputs=input_x, outputs=output_f)
    return model, model_features

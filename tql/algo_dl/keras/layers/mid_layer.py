#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : mid_layer
# @Time         : 2019-07-12 16:33
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 
"""
https://www.tensorflow.org/beta/tutorials/keras/feature_columns
"""

from tensorflow.python.keras.layers import Input, Embedding, Reshape, Activation
from tensorflow.python.keras.models import Model

input_model = Input(shape=(1,))
output_store = Embedding(1115, 10, name='store_embedding')(input_model)
output_store = Reshape(target_shape=(10,))(output_store)

output_model = Activation('sigmoid')(output_store)
model = Model(inputs=input_model, outputs=output_model)
model.summary()

embed = Model(inputs=model.input, outputs=model.get_layer(index=1).output)
# 以这个model的预测值作为输出
embed.predict([[1]])

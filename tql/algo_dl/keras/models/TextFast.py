#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : FastText
# @Time         : 2019-06-24 10:36
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

from .BaseModel import BaseModel
from tensorflow.python.keras import Input, Model
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.layers import GlobalAveragePooling1D


class TextFast(BaseModel):

    def __init__(self, max_tokens, maxlen=128, embedding_size=None, num_class=1, weights=None):
        super().__init__(max_tokens, maxlen, embedding_size, num_class, weights)

    def get_model(self):
        input = Input(self.maxlen)

        embedding = self.embedding_layer(input)
        x = GlobalAveragePooling1D()(embedding)

        output = Dense(self.num_class, activation=self.last_activation)(x)
        model = Model(inputs=input, outputs=output)
        return model

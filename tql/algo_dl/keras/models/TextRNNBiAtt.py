#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : TextRNNBiAtt
# @Time         : 2019-06-24 11:36
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

from .BaseModel import BaseModel
from tensorflow.python.keras import Input, Model
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.layers import Attention, AdditiveAttention
from tensorflow.python.keras.layers import Bidirectional, LSTM, CuDNNLSTM, GRU, CuDNNGRU


class TextRNNBiAtt(BaseModel):
    """
    TODO:
    """

    def __init__(self, max_tokens, maxlen=128, embedding_size=None, num_class=1, weights=None, rnn=GRU):
        """
        :param rnn: LSTM, CuDNNLSTM, GRU, CuDNNGRU
        """
        super().__init__(max_tokens, maxlen, embedding_size, num_class, weights)
        self._RNN = rnn

    def get_model(self):
        input = Input((self.maxlen,))

        embedding = self.embedding_layer(input)
        x = Bidirectional(self._RNN(128, return_sequences=True))(embedding)  # LSTM or GRU
        # TODO: keras 官方版 attention 怎么用
        x = Attention(self.maxlen)(x)

        output = Dense(self.num_class, activation=self.last_activation)(x)
        model = Model(inputs=input, outputs=output)
        return model

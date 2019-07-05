#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : TextRCNN
# @Time         : 2019-06-24 17:15
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

from .BaseModel import BaseModel
from tensorflow.python.keras import backend as K
from tensorflow.python.keras import Input, Model
from tensorflow.python.keras.layers import Dense, Embedding, Lambda, Concatenate
from tensorflow.python.keras.layers import Conv1D, GlobalMaxPooling1D
from tensorflow.python.keras.layers import Bidirectional, LSTM, CuDNNLSTM, GRU, CuDNNGRU


class TextRCNN(BaseModel):
    def __init__(self, max_tokens, maxlen=128, embedding_size=None, num_class=1, weights=None, rnn=CuDNNGRU):
        """
        :param rnn: LSTM, CuDNNLSTM, GRU, CuDNNGRU
        """
        super().__init__(max_tokens, maxlen, embedding_size, num_class, weights)
        self._RNN = rnn

    def get_model(self):
        input_current = Input((self.maxlen,))
        input_left = Input((self.maxlen,))
        input_right = Input((self.maxlen,))

        embedder = Embedding(self.max_tokens, self.embedding_size, input_length=self.maxlen)
        embedding_current = embedder(input_current)
        embedding_left = embedder(input_left)
        embedding_right = embedder(input_right)

        x_left = self._RNN(128, return_sequences=True)(embedding_left)
        x_right = self._RNN(128, return_sequences=True, go_backwards=True)(embedding_right)

        x_right = Lambda(lambda x: K.reverse(x, axes=1))(x_right)
        x = Concatenate(axis=2)([x_left, embedding_current, x_right])

        x = Conv1D(64, kernel_size=1, activation='tanh')(x)
        x = GlobalMaxPooling1D()(x)

        output = Dense(self.num_class, activation=self.last_activation)(x)
        model = Model(inputs=[input_current, input_left, input_right], outputs=output)
        return model

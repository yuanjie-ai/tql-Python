#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : TextRCNNVariant
# @Time         : 2019-06-24 17:22
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

from .BaseModel import BaseModel
from tensorflow.python.keras import backend as K
from tensorflow.python.keras import Input, Model
from tensorflow.python.keras.layers import Dense, Embedding, Lambda, Concatenate
from tensorflow.python.keras.layers import Conv1D, GlobalMaxPooling1D, GlobalAveragePooling1D
from tensorflow.python.keras.layers import Bidirectional, LSTM, CuDNNLSTM, GRU, CuDNNGRU


class TextRCNNVariant(BaseModel):
    """Variant of RCNN.
        Base on structure of RCNN, we do some improvement:
        1. Ignore the shift for left/right context.
        2. Use Bidirectional LSTM/GRU to encode context.
        3. Use Multi-CNN to represent the semantic vectors.
        4. Use ReLU instead of Tanh.
        5. Use both AveragePooling and MaxPooling.
    """

    def __init__(self, max_tokens, maxlen=128, embedding_size=None, num_class=1, weights=None,
                 kernel_size_list=range(1, 5)):
        """
        :param rnn: LSTM, CuDNNLSTM, GRU, CuDNNGRU
        """
        super().__init__(max_tokens, maxlen, embedding_size, num_class, weights)
        self.kernel_size_list = kernel_size_list

    def get_model(self):
        input = Input((self.maxlen,))

        embedding = Embedding(self.max_tokens, self.embedding_size, input_length=self.maxlen)(input)

        x_context = Bidirectional(CuDNNLSTM(128, return_sequences=True))(embedding)
        x = Concatenate()([embedding, x_context])

        convs = []
        for kernel_size in self.kernel_size_list:
            conv = Conv1D(128, kernel_size, activation='relu')(x)
            convs.append(GlobalMaxPooling1D()(conv))
            convs.append(GlobalAveragePooling1D()(conv))

        # poolings = [GlobalAveragePooling1D()(conv) for conv in convs] + \
        #            [GlobalMaxPooling1D()(conv) for conv in convs]
        x = Concatenate()(convs)

        output = Dense(self.num_class, activation=self.last_activation)(x)
        model = Model(inputs=input, outputs=output)
        return model

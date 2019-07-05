#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : TextCNN
# @Time         : 2019-06-21 18:56
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

from .BaseModel import BaseModel
from tensorflow.python.keras import Input, Model
from tensorflow.python.keras.layers import Dense, Concatenate, Dropout
from tensorflow.python.keras.layers import Conv1D, GlobalMaxPool1D, GlobalAvgPool1D


class TextCNN(BaseModel):
    """ TextCNN:
    1. embedding layers: embeddings = model.layers[0].get_weights()[0]
    2. convolution layer,
    3. max-pooling,
    4. softmax layer.
    数据量较大：可以直接随机初始化embeddings，然后基于语料通过训练模型网络来对embeddings进行更新和学习。
    数据量较小：可以利用外部语料来预训练(pre-train)词向量，然后输入到Embedding层，用预训练的词向量矩阵初始化embeddings。（通过设置weights=[embedding_matrix]）。
    静态(static)方式：训练过程中不再更新embeddings。实质上属于迁移学习，特别是在目标领域数据量比较小的情况下，采用静态的词向量效果也不错。（通过设置trainable=False）
    非静态(non-static)方式：在训练过程中对embeddings进行更新和微调(fine tune)，能加速收敛。（通过设置trainable=True）
    """

    def __init__(self, max_tokens, maxlen=128, embedding_size=None, num_class=1, kernel_size_list=(3, 4, 5),
                 weights=None):
        """

        :param embedding_size: 类别/实体嵌入时可不指定

        model = TextCNN(max_token, maxlen, num_class=1)()
        model.compile('adam', 'binary_crossentropy', metrics=['accuracy'])
        model.fit_generator(DataIter(X, y), epochs=5)
        """
        super().__init__(max_tokens, maxlen, embedding_size, num_class, weights)
        self.kernel_size_list = kernel_size_list

    def get_model(self):
        input = Input(self.maxlen)
        # Embedding part can try multichannel as same as origin paper
        embedding = self.embedding_layer(input)
        convs = []
        for kernel_size in self.kernel_size_list:
            c = Conv1D(128, kernel_size, activation='relu')(embedding)  # 卷积
            # c = Dropout(0.5)(c)
            p = GlobalMaxPool1D()(c)  # 池化
            # p = GlobalAvgPool1D()(c)
            convs.append(p)
        x = Concatenate()(convs)
        output = Dense(self.num_class, activation=self.last_activation)(x)

        model = Model(inputs=input, outputs=output)
        return model


if __name__ == '__main__':
    TextCNN(1000, 10)()

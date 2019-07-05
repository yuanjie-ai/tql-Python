#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : DataGenerator
# @Time         : 2019-06-20 17:22
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :


from sklearn.utils import shuffle


class DataGenerator(object):
    """
    https://blog.csdn.net/leviopku/article/details/87912097
    https://github.com/afshinea/keras-data-generator
    https://blog.csdn.net/u011311291/article/details/80991330
    """

    def __init__(self, X, y, batch_size=32, mapper=lambda *args: args):
        """

        :param X:
        :param y:
        :param batch_size:
        :param maxlen:
        :param is_train:
        :param mapper:
            # bert keras
            from keras.preprocessing.sequence import pad_sequences
            from keras_bert import load_trained_model_from_checkpoint, Tokenizer

            def mapper(X, y):
                X = list(map(lambda x: pad_sequences(x, 128), zip(*map(tokenizer.encode, X))))
                return X, y

        """
        self.X = X
        self.y = y
        self.batch_size = batch_size
        self.steps = (len(X) + batch_size - 1) // batch_size

        assert callable(mapper) is True
        self.mapper = mapper

    def __len__(self):
        return self.steps

    def __iter__(self):
        self.X, self.y = shuffle(self.X, self.y)
        while 1:
            for i in range(self.steps):
                idx_s = i * self.batch_size
                idx_e = (i + 1) * self.batch_size

                X = self.X[idx_s:idx_e]
                y = self.y[idx_s:idx_e]

                yield self.mapper(X, y)

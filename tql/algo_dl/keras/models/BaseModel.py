#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : BaseModel
# @Time         : 2019-06-22 22:21
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :

from pathlib import Path
from abc import abstractmethod
from tensorflow.python.keras.utils import plot_model as _plot_model
from tensorflow.python.keras.layers import Embedding


# import tensorflow as tf
# tf.keras.backend.clear_session()


class BaseModel(object):
    """
    https://github.com/ShawnyXiao/TextClassification-Keras
    """

    @abstractmethod
    def __init__(self, max_tokens=20000, maxlen=128, embedding_size=None, num_class=1, weights=None, **kwargs):
        self.max_tokens = max_tokens
        self.maxlen = maxlen
        self.embedding_size = embedding_size if embedding_size else min(50, (max_tokens + 1) // 2)  # 经验值

        self.num_class = num_class
        self.last_activation = 'softmax' if num_class > 1 else 'sigmoid'

        self.weights = weights

    def __call__(self, plot_model=None, dir='.', **kwargs):
        model = self.get_model()
        model.summary()
        if plot_model:
            image_file = Path(dir) / ('%s.png' % self._class_name)
            image_file = image_file.absolute().__str__()
            try:  # 必须return才能show图
                _plot_model(model, to_file=image_file, show_shapes=True, dpi=128)
            except Exception as e:
                print(e)
                print("brew install graphviz or apt-get install graphviz")
        return model

    @abstractmethod
    def get_model(self):
        pass

    def plot_show(self, image_file=None):
        if image_file is None:
            image_file = '%s.png' % self._class_name
        try:
            from IPython import display
            return display.Image(filename=image_file)
        except ImportError:
            pass

    @property
    def _class_name(self):
        return str(self).split(maxsplit=1)[0][10:]

    @property
    def embedding_layer(self):
        if self.weights is not None:
            return Embedding(*self.weights.shape, input_length=self.maxlen, weights=[self.weights], trainable=False)
        else:
            return Embedding(self.max_tokens, self.embedding_size, input_length=self.maxlen)


if __name__ == '__main__':
    bm = BaseModel()
    print(bm._class_name)

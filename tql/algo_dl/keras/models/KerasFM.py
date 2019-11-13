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
import pandas as pd
from tensorflow.python.keras.models import Model
from tensorflow.python.keras.layers.normalization import BatchNormalization
from tensorflow.python.keras.layers import Input, Embedding, Dense, Flatten, Concatenate, Dot, Reshape, Add, Subtract
from tensorflow.python.keras.optimizers import Adam
from tensorflow.python.keras.regularizers import l2
from tensorflow.python.keras.callbacks import EarlyStopping, ModelCheckpoint


class KerasFM(object):

    def __init__(self, k_latent=2, kernel_l2=0.1):
        self.k_latent = k_latent  # TODO: embedding dim 经验值
        self.kernel_l2 = kernel_l2

    def build_model(self, f_sizes):
        """
        :param f_size: sparse feature nunique
        :return:
        """
        dim_input = len(f_sizes)  # +1

        input_x = [Input(shape=(1,)) for i in range(dim_input)]  # 多列 sparse feature
        biases = [self.get_embed(x, size, 1) for (x, size) in zip(input_x, f_sizes)]
        factors = [self.get_embed(x, size) for (x, size) in zip(input_x, f_sizes)]

        s = Add()(factors)
        diffs = [Subtract()([s, x]) for x in factors]
        dots = [Dot(axes=1)([d, x]) for d, x in zip(diffs, factors)]

        x = Concatenate()(biases + dots)
        x = BatchNormalization()(x)
        output = Dense(1, activation='relu', kernel_regularizer=l2(self.kernel_l2))(x)
        model = Model(inputs=input_x, outputs=[output])
        model.compile(optimizer=Adam(clipnorm=0.5), loss='mean_squared_error')  # TODO: radam

        output_f = factors + biases
        model_features = Model(inputs=input_x, outputs=output_f)
        return model, model_features

    def get_embed(self, x_input, x_size, embedding_l2=0.0002):
        if x_size > 0:  # category
            embed = Embedding(x_size, self.k_latent, input_length=1, embeddings_regularizer=l2(embedding_l2))(x_input)
            embed = Flatten()(embed)
        else:
            embed = Dense(self.k_latent, kernel_regularizer=l2(embedding_l2))(x_input)
        return embed

    def get_factors_biases(self, Xs, feature_names, model_features):
        """We can now retrieve the factors and the biases"""
        X_pred = model_features.predict(Xs, 2 ** 10)
        n = len(X_pred) // 2
        factors = X_pred[:n]
        biases = X_pred[-n:]

        df = pd.DataFrame()
        for f, X_p in zip(feature_names, factors):
            for i in range(self.k_latent):
                df[f'{f}_fm_factor_{i}'] = X_p[:, i]

        for f, X_p in zip(feature_names, biases):
            df[f'{f}_fm_bias'] = X_p[:, 0]
        return df


if __name__ == '__main__':
    from sklearn.datasets import make_classification
    from sklearn.preprocessing import LabelEncoder

    X, y = make_classification(n_samples=1000, n_features=7, random_state=42)

    Xs = []
    f_sizes = []
    for i in range(X.shape[1]):
        X[:, i] = LabelEncoder().fit_transform(X[:, i])
        f_sizes.append(int(X[:, i].max() + 1))
        Xs.append(X[:, i])

    print(f_sizes)
    fm = KerasFM()
    model, model_features = fm.build_model(f_sizes)
    earlystopper = EarlyStopping(patience=0, verbose=1)
    model.fit(Xs, y.ravel(), epochs=10,
              batch_size=2 ** 7,
              verbose=1,
              shuffle=True,
              sample_weight=None,
              callbacks=[earlystopper],
              )
    df_ = fm.get_factors_biases(Xs, range(len(Xs)), model_features)
    print(df_)
    print(df_.shape) # n_features * 3

    print(model.predict(Xs))
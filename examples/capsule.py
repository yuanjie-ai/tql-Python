#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : capsule
# @Time         : 2019-07-10 16:41
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


from tensorflow.python.keras import utils
from tensorflow.python.keras.datasets import mnist
from tensorflow.python.keras.models import Model
from tensorflow.python.keras.layers import *
from tensorflow.python.keras import backend as K
import numpy as np
from tql.algo_dl.keras.models.Capsule import Capsule

# 准备训练数据
batch_size = 128
num_classes = 10
img_rows, img_cols = 28, 28

(x_train, y_train), (x_test, y_test) = mnist.load_data() # '../../../fds/data/mnist.npz'
x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)

x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255
y_train = utils.to_categorical(y_train, num_classes)
y_test = utils.to_categorical(y_test, num_classes)

# 准备自定义的测试样本
# 对测试集重新排序并拼接到原来测试集，就构成了新的测试集，每张图片有两个不同数字
idx = list(range(len(x_test)))
np.random.shuffle(idx)
X_test = np.concatenate([x_test, x_test[idx]], 1)
Y_test = np.vstack([y_test.argmax(1), y_test[idx].argmax(1)]).T
X_test = X_test[Y_test[:, 0] != Y_test[:, 1]]  # 确保两个数字不一样
Y_test = Y_test[Y_test[:, 0] != Y_test[:, 1]]
Y_test.sort(axis=1)  # 排一下序，因为只比较集合，不比较顺序

# 搭建CNN+Capsule分类模型
input_image = Input(shape=(None, None, 1))
cnn = Conv2D(64, (3, 3), activation='relu')(input_image)
cnn = Conv2D(64, (3, 3), activation='relu')(cnn)
cnn = AveragePooling2D((2, 2))(cnn)
cnn = Conv2D(128, (3, 3), activation='relu')(cnn)
cnn = Conv2D(128, (3, 3), activation='relu')(cnn)
cnn = Reshape((-1, 128))(cnn)
capsule = Capsule(10, 16, 3, True)(cnn)
output = Lambda(lambda x: K.sqrt(K.sum(K.square(x), 2)), output_shape=(10,))(capsule)

model = Model(inputs=input_image, outputs=output)
model.compile(
    loss=lambda y_true, y_pred: y_true * K.relu(0.9 - y_pred) ** 2 + 0.25 * (1 - y_true) * K.relu(y_pred - 0.1) ** 2,
    optimizer='adam',
    metrics=['accuracy'])

model.summary()

model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=10,
          verbose=1,
          validation_data=(x_test, y_test))

Y_pred = model.predict(X_test)  # 用模型进行预测
greater = np.sort(Y_pred, axis=1)[:, -2] > 0.5  # 判断预测结果是否大于0.5
Y_pred = Y_pred.argsort()[:, -2:]  # 取最高分数的两个类别
Y_pred.sort(axis=1)  # 排序，因为只比较集合

acc = 1.*(np.prod(Y_pred == Y_test, axis=1)).sum()/len(X_test)
print ('CNN+Capsule，不考虑置信度的准确率为：%s'%acc)
acc = 1.*(np.prod(Y_pred == Y_test, axis=1)*greater).sum()/len(X_test)
print ('CNN+Capsule，考虑置信度的准确率为：%s'%acc)
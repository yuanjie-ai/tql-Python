#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : keras
# @Time         : 2019-09-27 14:23
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 
"""https://stackoverflow.com/questions/43368241/student-teacher-model-in-keras/43700164"""

import keras
from keras.datasets import mnist
from keras.layers import Input, Embedding, LSTM, Dense, Lambda
from keras.models import Model
import numpy as np
from keras.utils import np_utils
from keras.layers.core import Dense, Dropout, Activation
from keras.models import Sequential
from keras.layers import Dense, Merge
from keras.optimizers import SGD, Adam, RMSprop
from keras.layers import *

nb_classes = 10

(X_train, y_train), (X_test, y_test) = mnist.load_data()

X_train = X_train.reshape(60000, 784)
X_test = X_test.reshape(10000, 784)
X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
X_train /= 255
X_test /= 255
print(X_train.shape[0], 'train samples')
print(X_test.shape[0], 'test samples')

# convert class vectors to binary class matrices
Y_train = np_utils.to_categorical(y_train, nb_classes)
Y_test = np_utils.to_categorical(y_test, nb_classes)



batch_size = 128
nb_classes = 10
nb_epoch = 3

teacher = Sequential()
teacher.add(Dense(10, input_shape=(784,)))
teacher.add(Dense(10))
teacher.add(Activation('softmax'))

teacher.summary()
teacher.compile(loss='categorical_crossentropy',
                optimizer=RMSprop(),
                metrics=['accuracy'])

history = teacher.fit(X_train, Y_train,
                      batch_size=batch_size, nb_epoch=nb_epoch,
                      verbose=1, validation_data=(X_test, Y_test))
score = teacher.evaluate(X_test, Y_test, verbose=0)
print('Test score:', score[0])
print('Test accuracy:', score[1])

for i in range(len(teacher.layers)):
    setattr(teacher.layers[i], 'trainable', False)

Y_train = np.zeros((60000, 10))

student = Sequential()
student.add(Dense(10, input_dim=784))
student.add(Activation('softmax'))
student.compile(loss='mean_squared_error', optimizer='Adam', metrics=['accuracy'])



def negativeActivation(x):
    return -x


negativeRight = Activation(negativeActivation)(student.output)
diff = Add()([teacher.output, negativeRight])

model = Model(inputs=[teacher.input, student.input], outputs=[diff])
model.compile(loss='mean_squared_error', optimizer='Adam', metrics=['acc'])

model.summary(line_length=150)
model.fit([X_train, X_train], [Y_train], batch_size=128, nb_epoch=5)

print
student.evaluate(X_test, Y_test)

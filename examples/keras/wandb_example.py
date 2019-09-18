#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : wandb_example
# @Time         : 2019-08-12 13:29
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


from tensorflow.python.keras.datasets import fashion_mnist
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Conv2D, MaxPooling2D, Dropout, Dense, Flatten
from tensorflow.python.keras.utils import np_utils
from tensorflow.python.keras.optimizers import SGD
from tensorflow.python.keras.callbacks import TensorBoard
import random

# Import wandb libraries
import wandb
from wandb.keras import WandbCallback

# Initialize wandb
wandb.init(project="example")
config = wandb.config


# Track hyperparameters
config.dropout = 0.2
config.hidden_layer_size = 128
config.layer_1_size = 16
config.layer_2_size = 32
config.learn_rate = 0.01
config.decay = 1e-6
config.momentum = 0.9
config.epochs = 8

(X_train_orig, y_train_orig), (X_test, y_test) = fashion_mnist.load_data()

# Reducing the dataset size to 10,000 examples for faster train time
true = list(map(lambda x: True if random.random() < 0.167 else False, range(60000)))
ind = []
for i, x in enumerate(true):
    if x == True: ind.append(i)

X_train = X_train_orig[ind, :, :]
y_train = y_train_orig[ind]

img_width = 28
img_height = 28
labels = ["T-shirt/top", "Trouser", "Pullover", "Dress",
          "Coat", "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"]

X_train = X_train.astype('float32')
X_train /= 255
X_test = X_test.astype('float32')
X_test /= 255

# reshape input data
X_train = X_train.reshape(X_train.shape[0], img_width, img_height, 1)
X_test = X_test.reshape(X_test.shape[0], img_width, img_height, 1)

# one hot encode outputs
y_train = np_utils.to_categorical(y_train)
y_test = np_utils.to_categorical(y_test)
num_classes = y_test.shape[1]

sgd = SGD(lr=config.learn_rate, decay=config.decay, momentum=config.momentum,
          nesterov=True)

# build model
model = Sequential()
model.add(Conv2D(config.layer_1_size, (5, 5), activation='relu',
                 input_shape=(img_width, img_height, 1)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(config.layer_2_size, (5, 5), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(config.dropout))
model.add(Flatten())
model.add(Dense(config.hidden_layer_size, activation='relu'))
model.add(Dense(num_classes, activation='softmax'))

# Add Keras WandbCallback
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=config.epochs,
          callbacks=[WandbCallback(data_type="image", labels=labels)])

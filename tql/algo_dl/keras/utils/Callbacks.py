#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : Callbacks
# @Time         : 2019-07-10 17:27
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 
from tensorflow.python.keras.callbacks import *


# ModelCheckpoint, LearningRateScheduler, EarlyStopping, ReduceLROnPlateau

class Callbacks(object):

    def __init__(self):
        self.callbacks = [self.checkpointer, self.lr_reducing, self.early_stopping]

    @property
    def checkpointer(self):
        # filepath="weights-improvement-{epoch}-{val_acc:.2f}.hdf5" # 多个check point
        return ModelCheckpoint("best_model_weights.hdf5", verbose=1, save_best_only=True)

    @property
    def lr_reducing(self):
        """Dynamic learning rate"""
        annealer = LearningRateScheduler(lambda x: 0.01 * 0.9 ** x)
        #         annealer = ReduceLROnPlateau(factor=0.1, patience=3, verbose=1) # lr = lr*0.9
        return annealer

    @property
    def early_stopping(self):
        return EarlyStopping(patience=3, verbose=1)

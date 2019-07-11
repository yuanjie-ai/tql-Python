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


# RemoteMonitor, ModelCheckpoint, LearningRateScheduler, EarlyStopping, ReduceLROnPlateau

class Callbacks(object):
    """
    https://blog.csdn.net/dayuqi/article/details/85090353
    """

    def __init__(self, early_stopping_epochs=4, monitor='val_loss', save_weights_only=False,
                 weightsfile="best_model_weights.hdf5"):
        self.monitor = monitor
        self.weightsfile = weightsfile
        self.save_weights_only = save_weights_only  # 默认保存模型
        self.early_stopping_epochs = early_stopping_epochs
        self.callbacks = [self.checkpointer, self.lr_reducing, self.early_stopping]

    def tensorboard(self, log_dir='logs'):
        """tensorboard --logdir=/full_path_to_your_logs"""
        TensorBoard(log_dir,
                    histogram_freq=0,
                    write_graph=True,
                    write_images=False,
                    update_freq='epoch',
                    profile_batch=2,
                    embeddings_freq=0,
                    embeddings_metadata=None)

    @property
    def checkpointer(self):
        """
        save_freq=128相当于一步判断一次（按样本数更新保存最优权重）
        """
        # filepath="weights-improvement-{epoch}-{val_acc:.2f}.hdf5" # 多个check point
        return ModelCheckpoint(filepath=self.weightsfile,
                               monitor=self.monitor,
                               save_best_only=True,
                               save_weights_only=self.save_weights_only,
                               save_freq='epoch',
                               verbose=1)

    @property
    def lr_reducing(self):
        """动态学习率"""
        # new_lr = old_lr * self.factor
        annealer = ReduceLROnPlateau(factor=0.9, patience=2, verbose=1, min_lr=0.0001)
        # annealer = LearningRateScheduler(lambda x: min(0.01 * 0.9 ** x, 0.001), verbose=1)
        return annealer

    @property
    def early_stopping(self):
        """patience次没提高就停止"""
        return EarlyStopping(patience=self.early_stopping_epochs,
                             restore_best_weights=True,
                             verbose=1)

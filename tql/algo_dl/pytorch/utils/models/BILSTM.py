#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : BILSTM
# @Time         : 2019-12-27 14:05
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 
# import keras
# keras.preprocessing.text.hashing_trick

import torch
import torch.nn as nn
import torch.nn.functional as F


class Config(object):
    # Data
    class_num = 2

    # Embedding
    pretrained_embedding = None  # pretrained_weight
    vocab_dim = 128 if pretrained_embedding is None else pretrained_embedding.shape[1]
    vocab_size = 10000

    # RNN
    rnn_layers_num = 2
    rnn_dropout = 0

    # Linear
    fc_dropout = 0


opt = Config()


class BiLSTM(nn.Module):
    def __init__(self):
        super(BiLSTM, self).__init__()
        # self.embed = nn.Embedding(V, D, max_norm=config.max_norm)
        self.embed = nn.Embedding(opt.vocab_size, opt.vocab_dim)
        # pretrained  embedding
        if opt.pretrained_embedding:
            self.embed.weight.data.copy_(opt.pretrained_embedding)
            # self.embed.weight.requires_grad = False  # 冻结词向量

        self.bilstm = nn.LSTM(
            opt.vocab_dim,
            opt.vocab_dim // 2,
            dropout=opt.rnn_dropout,
            num_layers=opt.rnn_layers_num,
            batch_first=True,  # input & output will has batch size as 1s dimension. e.g. (batch, time_step, input_size)
            bidirectional=True)
        print(self.bilstm)

        self.fc1 = nn.Linear(opt.vocab_dim // 2 * 2, opt.vocab_dim // 2)
        self.fc2 = nn.Linear(opt.vocab_dim // 2, opt.class_num)
        self.dropout = nn.Dropout(opt.fc_dropout)

    def forward(self, x):
        embed = self.embed(x)
        x = embed.view(len(x), embed.size(1), -1)
        # x shape (batch, time_step, input_size)
        # r_out shape (batch, time_step, output_size)
        # h_n shape (n_layers, batch, hidden_size)
        # h_c shape (n_layers, batch, hidden_size)
        r_out, (h_n, h_c) = self.bilstm(x)
        r_out = F.relu(r_out)

        # r_out = F.max_pool1d(r_out, r_out.size(2)).squeeze(2)
        # y = self.fc1(r_out)
        # y = self.fc2(y)
        # choose r_out at the last time step
        y = self.fc1(r_out[:, -1, :])
        y = self.fc2(y)
        return torch.softmax(y)

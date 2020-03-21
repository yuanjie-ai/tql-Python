#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : lr
# @Time         : 2020-02-22 11:24
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

import torch
import torch.nn as nn
import torch.nn.functional as F


class BiLSTM(nn.Module):
    def __init__(self):
        super().__init__()


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

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'CustomDataset'
__author__ = 'JieYuan'
__mtime__ = '2019/4/17'
"""
import torch
from torch.utils.data import Dataset, DataLoader, TensorDataset


def loader(X, y, batch_size, shuffle=True):
    _ = DataLoader(TensorDataset(X, y), batch_size=batch_size, shuffle=shuffle)
    return _


class CustomDataset(Dataset):

    # Initialize your data, download, etc.
    def __init__(self, X, y=None):
        self.X = torch.from_numpy(X)
        self.y = y
        if y is not None:
            self.y = torch.from_numpy(y)

    def __getitem__(self, index):
        if self.y is not None:
            return self.X[index], self.y[index]
        else:
            return self.X[index]

    def __len__(self):
        return self.X.shape[0]

    @classmethod
    def load(cls, X, y=None, batch_size=32, shuffle=True, drop_last=False):
        loader = DataLoader(
            dataset=cls(X, y),
            batch_size=batch_size,
            shuffle=shuffle,
            drop_last=drop_last
        )
        return loader

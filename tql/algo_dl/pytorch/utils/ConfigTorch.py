#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'TorchConfig'
__author__ = 'JieYuan'
__mtime__ = '2019/4/17'
"""

import os
import torch
import random
import numpy as np


class TorchConfig(object):
    """Hyper-parameters"""

    input_size = 784
    hidden_size = 500
    num_classes = 10

    num_epochs = 5
    batch_size = 128
    lr = 0.001

    def __init__(self, seed=2019):
        torch.cuda.empty_cache()
        self._seed = seed
        self.use_cuda = torch.cuda.is_available()
        self.device = torch.device('cuda' if self.use_cuda else 'cpu')  # Device configuration
        self.set_seed()
        # torch.set_default_tensor_type(torch.DoubleTensor)

    def set_seed(self):
        os.environ['PYTHONHASHSEED'] = '0'
        random.seed(self._seed)
        np.random.seed(self._seed)
        torch.manual_seed(self._seed)
        if self.use_cuda:
            print('GPU: %s' % torch.cuda.get_device_name(0))
            torch.cuda.manual_seed(self._seed)
            # torch.backends.cudnn.benchmark = True # Benchmark 模式会提升计算速度，但是由于计算中有随机性，每次网络前馈结果略有差异。
            torch.backends.cudnn.deterministic = True  # 避免这种结果波动

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
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')  # Device configuration
        # torch.set_default_tensor_type(torch.DoubleTensor)
        # set seed
        os.environ['PYTHONHASHSEED'] = '0'
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        torch.cuda.manual_seed(seed)

        if torch.cuda.is_available():
            print('GPU: %s' % torch.cuda.get_device_name(0))
            torch.backends.cudnn.benchmark = True  # Benchmark 模式会提升计算速度，但是由于计算中有随机性，每次网络前馈结果略有差异。
            torch.backends.cudnn.deterministic = True  # 避免这种结果波动

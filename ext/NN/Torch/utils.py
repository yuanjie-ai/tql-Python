#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'utils'
__author__ = 'JieYuan'
__mtime__ = '2019/4/12'
"""

import os
import torch
import random
import numpy as np


class TorchConfig(object):
    USE_CUDA = torch.cuda.is_available()

    def __init__(self, seed=2019):
        self.seed = seed
        self.device = torch.device('cuda' if self.USE_CUDA else 'cpu')
        self.set_seed()

    def set_seed(self):
        os.environ['PYTHONHASHSEED'] = str(self.seed)
        random.seed(self.seed)
        np.random.seed(self.seed)
        torch.manual_seed(self.seed)
        if self.USE_CUDA:
            torch.cuda.manual_seed(self.seed)
            torch.backends.cudnn.deterministic = True

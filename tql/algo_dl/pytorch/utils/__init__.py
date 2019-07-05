#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '__init__.py'
__author__ = 'JieYuan'
__mtime__ = '2019/4/17'
"""
import torch

from .ConfigTorch import TorchConfig
from .CustomDataset import CustomDataset
from .WeightInit import WeightInit


#################################################################

def torch_save(model_cls, model_pt):
    torch.save(model_cls.state_dict(), model_pt)


def torch_load(model_cls, model_pt):
    model_cls.load_state_dict(torch.load(model_pt))


# 类绑定方法
# https://www.cnblogs.com/seirios1993/p/6624157.html
class Model:

    @classmethod
    def load(cls, params_path='params.ckpt'):
        model = cls()
        model.load_state_dict(torch.load(params_path))

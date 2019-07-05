#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'weights_init'
__author__ = 'JieYuan'
__mtime__ = '2019/4/17'
"""

from torch.nn import init


class WeightInit(object):

    def __init__(self, layers=['Linear']):
        self.layers = layers

    def __call__(self, model):
        return self._fn(model)

    def _fn(self, model):
        classname = model.__class__.__name__
        # 对layers中包含的层初始化
        if any(map(lambda layer: classname.find(layer) != -1, self.layers)):
            init.xavier_normal_(model.weight.data)
            init.constant_(model.bias.data, 0.0)


if __name__ == '__main__':
    from torch import nn


    class Net(nn.Module):
        pass


    # apply函数会递归地搜索网络内的所有module并把参数表示的函数应用到所有的module上。
    # 对所有的Conv层都初始化权重.
    net = Net()
    net.apply(WeightInit(layers=['Conv']))

    # def weights_init(model, layers):
    #     classname = model.__class__.__name__
    #     # 对layers中包含的层初始化
    #     if any(map(lambda layer: classname.find(layer) != -1, layers)):
    #         init.xavier_normal_(model.weight.data)
    #         init.constant_(model.bias.data, 0.0)
    # from functools import partial
    # weights_init = partial(weights_init, layers=['Conv'])
    # net.apply(weights_init)

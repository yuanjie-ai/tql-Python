#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'fire'
__author__ = 'JieYuan'
__mtime__ = '19-1-10'
"""

import fire


class Config(object):
    """默认参数"""
    x = 1
    y = 2
    z = 3


opt = Config()


def gen(**kwargs):
    for item in kwargs.items():
        setattr(opt, *item)

    _ = opt.x + opt.y + opt.z  # 操作逻辑
    return _


if __name__ == '__main__':
    fire.Fire()  # python ./fire_args.py gen --x 100
    # fire.Fire() # python fire_args.py --x 10000

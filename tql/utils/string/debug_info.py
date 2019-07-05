#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'debug_info'
__author__ = 'JieYuan'
__mtime__ = '19-1-29'
"""
from datetime import datetime

"""强大的日志模块loguru"""


def debug_info(message='message', level=0):
    _level = {
        0: 'INFO',
        1: 'WARNING',
        2: 'DEBUG'
    }
    return f"{datetime.now()} | {_level[level]}: {message}"

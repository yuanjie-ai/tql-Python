#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '__init__.py'
__author__ = 'JieYuan'
__mtime__ = '18-12-17'
"""

from .string import cprint, cstring

group_by_step = lambda ls, step=3: [ls[idx: idx + step] for idx in range(0, len(ls), step)]

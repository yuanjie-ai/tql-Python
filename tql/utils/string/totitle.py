#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'title'
__author__ = 'JieYuan'
__mtime__ = '19-3-8'
"""
import re


def tile(s):
    return re.sub('[^0-9a-zA-Z]+', '_', s).title()

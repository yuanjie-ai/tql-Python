#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '__init__.py'
__author__ = 'JieYuan'
__mtime__ = '19-1-2'
"""
import re

chinese = re.compile('[\u4e00-\u9fa5]+')
_chinese = re.compile('[^\u4e00-\u9fa5]+')

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '__init__.py'
__author__ = 'JieYuan'
__mtime__ = '19-3-18'
"""
import os

from .multi_read_csv import multi_read_csv
from .read2write import read2write

base_dir = os.path.dirname(os.path.realpath('__file__'))
get_module_path = lambda path, file: os.path.normpath(os.path.join(os.getcwd(), os.path.dirname(file), path))

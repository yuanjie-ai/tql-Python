#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'timer'
__author__ = 'JieYuan'
__mtime__ = '19-1-14'
"""
import time
from contextlib import contextmanager

from .. import cprint


@contextmanager
def timer(task_name="timer"):
    # a timer cm from https://www.kaggle.com/lopuhin/mercari-golf-0-3875-cv-in-75-loc-1900-s
    print('\n')
    cprint(">>> {} started".format(task_name))
    t0 = time.time()
    yield
    cprint(">>> {} done in {:.0f} seconds".format(task_name, time.time() - t0))


if __name__ == '__main__':
    with timer() as t:
        print('xxx')

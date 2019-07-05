#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : timer
# @Time         : 2019-06-20 11:26
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :
import time
from contextlib import contextmanager

from .. import cprint


@contextmanager
def timer(task_name="timer"):
    # a timer cm from https://www.kaggle.com/lopuhin/mercari-golf-0-3875-cv-in-75-loc-1900-s
    cprint(">>> {} started".format(task_name))
    t0 = time.time()
    yield
    cprint(">>> {} done in {:.0f} seconds".format(task_name, time.time() - t0))

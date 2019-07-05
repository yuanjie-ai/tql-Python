#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'limit_memory'
__author__ = 'JieYuan'
__mtime__ = '19-3-15'
"""
import resource


def limit_memory(memory=16):
    """
    :param memory: 默认限制内存为 16G
    :return:
    """
    rsrc = resource.RLIMIT_AS
    # res_mem=os.environ["RESOURCE_MEM"]
    memlimit = memory * 1024 ** 3
    resource.setrlimit(rsrc, (memlimit, memlimit))
    # soft, hard = resource.getrlimit(rsrc)
    print("memory limit as: %s G" % memory)
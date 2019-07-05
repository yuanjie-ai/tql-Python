#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'SparkInit'
__author__ = 'JieYuan'
__mtime__ = '2019-05-13'
"""

from pyspark.sql import *


class SparkInit(object):
    """
    from pyspark.sql.types import *
    import pyspark.sql.functions as F
    """

    def __init__(self):
        """
        sc, spark = SparkInit()()
        """
        self.spark = SparkSession.builder \
            .appName("Yuanjie") \
            .config('log4j.rootCategory', "WARN") \
            .enableHiveSupport() \
            .getOrCreate()

        self.sc = self.spark.sparkContext
        print('Spark Version: %s' % self.spark.version)

    def __call__(self, *args, **kwargs):
        return self.sc, self.spark

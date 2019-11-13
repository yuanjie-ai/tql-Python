#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : demo
# @Time         : 2019-11-04 10:03
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


from tql.pipe import *

from tql.spark import SparkInit

from pyspark.sql.types import *
import pyspark.sql.functions as F

sc, spark = SparkInit()()
dd = spark.range(10).withColumn('v', F.lit(1))
dd.write.json('xx.json')
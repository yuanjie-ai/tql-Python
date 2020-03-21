#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : libsvm2df
# @Time         : 2020-01-22 12:16
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : https://blog.csdn.net/weixin_42286026/article/details/84496896


from pyspark.mllib.util import MLUtils

sc = ''
(
    MLUtils.loadLibSVMFile(sc, 'libsvm__')
        .map(lambda r: (r.label, r.features.toArray()))
        .saveAsTextFile('ffm')
)

from pyspark.mllib.regression import LabeledPoint
labelpointRDD = sparkdf.rdd.map(lambda row:LabeledPoint(row[-1], row[:-1]))
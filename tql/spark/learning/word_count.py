#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : word_count
# @Time         : 2019-08-08 10:10
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


from tql.spark import SparkInit

sc, spark = SparkInit()()
tf = (sc.textFile('./corpus.txt')
 .flatMap(lambda line: line.split(" "))
 .map(lambda word: (word, 1))
 .reduceByKey(lambda a, b: a + b)
 .collect())


print(sorted(tf, key=lambda x: - x[1]))
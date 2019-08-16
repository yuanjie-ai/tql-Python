#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : train_lgb
# @Time         : 2019-07-30 16:08
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

from tql.spark import SparkInit
import pyspark
from pyspark.sql.types import *

import pyspark.sql.functions as F
from pyspark.ml.feature import Word2Vec

spark = pyspark.sql.SparkSession.builder.appName("MyApp") \
    .config("spark.jars.packages", "Azure:mmlspark:0.17") \
    .getOrCreate()

from mmlspark import LightGBMClassifier
from pyspark.ml.classification import LogisticRegression
from sklearn.datasets import make_classification
import pandas as pd

X, y = make_classification()
df_pandas = pd.DataFrame(X).assign(label=y)
df_pandas.columns = [str(i) for i in df_pandas.columns]
df = spark.createDataFrame(df_pandas)

model = mmlspark.TrainClassifier(model=LightGBMClassifier(), labelCol='label').fit(df)
prediction = model.transform(df)
prediction.show()
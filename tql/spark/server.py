#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : server
# @Time         : 2019-07-30 18:56
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


import pyspark
from pyspark.sql.types import *

import pyspark.sql.functions as F
from pyspark.ml.feature import Word2Vec

spark = pyspark.sql.SparkSession.builder.appName("MyApp") \
    .config("spark.jars.packages", "Azure:mmlspark:0.17") \
    .getOrCreate()

from sklearn.datasets import make_classification
import pandas as pd

X, y = make_classification(n_features=4)
df_pandas = pd.DataFrame(X).assign(label=y)
df_pandas.columns = [str(i) for i in df_pandas.columns]
df = spark.createDataFrame(df_pandas)

from pyspark.ml.classification import LogisticRegression
from mmlspark import LightGBMClassifier, TrainClassifier, ComputeModelStatistics

model = TrainClassifier(model=LogisticRegression(), labelCol='label').fit(df)

from pyspark.sql.types import *
import uuid

serving_inputs = spark.readStream.server() \
    .address("0.0.0.0", 8899, "my_api") \
    .option("name", "my_api") \
    .load() \
    .parseRequest("my_api", df.schema)

serving_outputs = model.transform(serving_inputs) \
    .makeReply("scored_labels")

server = serving_outputs.writeStream \
    .server() \
    .replyTo("my_api") \
    .queryName("my_query") \
    .option("checkpointLocation", "file:///tmp/checkpoints-{}".format(uuid.uuid1())) \
    .start()

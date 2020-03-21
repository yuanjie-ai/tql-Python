#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : xx
# @Time         : 2020-02-23 22:40
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


import os

for i in range(1, 60)[::-1]:
    _ = f"""
    spark-submit --cluster 'zjyprc-hadoop-spark2.1' \
    --master yarn-cluster \
    --conf spark.speculation=false \
    --name com.xiaomi.algo.push.data.idmapping.XKpushJoin \
    --conf spark.yarn.job.owners=yuanjie \
    --conf spark.yarn.alert.phone.number=18550288233 \
    --queue 'production.miui_group.browser.miui_browser_zjy_1' \
    --num-executors 128 \
    --executor-cores 2 \
    --executor-memory 6g \
    --driver-memory 3g \
    --class com.xiaomi.algo.push.data.idmapping.XKpushJoinS \
    hdfs://zjyprc-hadoop/user/h_browser/algo/yuanjie/jars/MIPush-1.0-SNAPSHOT.jar \
    -delta=%s
    """ % i
    print(_.strip())
    os.system(_.strip())

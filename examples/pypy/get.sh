#!/usr/bin/env bash
# @Project      : tql-Python
# @Time         : 2019-08-27 14:04
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : ${DESCRIPTION}

hdfspath=hdfs://zjyprc-analysis/user/sql_prc/warehouse/kudu_demo.db/h_fenqun_3844_20190827
hdfs --cluster zjyprc-hadoop dfs -getmerge $hdfspath ./ata
hdfs --cluster zjyprc-hadoop dfs -put -f ./data  /user/h_browser/algo/yuanjie/UserGroups/军事

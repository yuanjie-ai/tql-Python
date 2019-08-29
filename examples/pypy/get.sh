#!/usr/bin/env bash
# @Project      : tql-Python
# @Time         : 2019-08-27 14:04
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : ${DESCRIPTION}

cd /home/work/yuanjie/checkpoint
dateStr=`date -d "-1 day" +"%Y%m%d"`
hdfspath=hdfs://zjyprc-analysis/user/sql_prc/warehouse/kudu_demo.db/h_fenqun_3844_$dateStr
hdfs --cluster zjyprc-hadoop dfs -getmerge $hdfspath ./data
hdfs --cluster zjyprc-hadoop dfs -put -f ./data  /user/h_browser/algo/yuanjie/UserGroups/军事/date=$dateStr

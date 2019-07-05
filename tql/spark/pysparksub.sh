#!/usr/bin/env bash
# @Project      : iWork
# @Time         : 2019-06-14 15:25
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : ${DESCRIPTION}

echo "jar: $1"
echo "mainclass: $2"

MAIN=$1

CLUSTER='zjyprc-hadoop'
QUEUE='production.miui_group.browser.miui_browser_zjy_1' # 'production.miui_group.browser.browser_1'
AUTHOR='yuanjie'
PHONE='18550288233'
EMAIL=$AUTHOR

#######################################################
~/infra-client/bin/pyspark-submit --verbose \
--cluster $CLUSTER \
--master yarn-cluster \
--queue $QUEUE \
--num-executors 100 \
--executor-cores 2 \
--executor-memory 6g \
--driver-memory 6g \
--conf spark.yarn.job.owners=$AUTHOR \
--conf spark.yarn.alert.phone.number=$PHONE \
--conf spark.yarn.alert.mail.address=$EMAIL \
$MAIN
# --py-files *.zip/*.py \

#######################################################




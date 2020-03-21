#!/usr/bin/env bash
# @Project      : tql-Python
# @Time         : 2020-01-22 13:45
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : ${DESCRIPTION}


#day_now=`date     -d "$1 days ago"          +"%Y%m%d%H%M"`
#day_today=`date   -d "$1 days ago"          +"%Y%m%d"`

#day_now="201908281811"
day_now=`date     -d "0 days ago"          +"%Y%m%d%H%M"`

#day_today="20190828"
day_today=`date   -d "0 days ago"          +"%Y%m%d"`

today_year=`date     -d "${day_today}" +"%Y"`
today_month=`date    -d "${day_today}" +"%m"`
today_day=`date      -d "${day_today}" +"%d"`
echo "day_now:         " ${day_now}
echo "day_today:       " ${day_today}
echo "today_year:      " ${today_year}
echo "today_month:     " ${today_month}
echo "today_day:       " ${today_day}

yesterday=`date +%Y%m%d  -d "${day_today} -1 days"`
yesterday_year=`date     -d "$yesterday" +"%Y"`
yesterday_month=`date    -d "$yesterday" +"%m"`
yesterday_day=`date      -d "$yesterday" +"%d"`
echo "yesterday:       " ${yesterday}
echo "yesterday_year:  " ${yesterday_year}
echo "yesterday_month: " ${yesterday_month}
echo "yesterday_day:   " ${yesterday_day}

#######super parameters which have to be set befor training#######
days_sample=10
echo "days_sample:   " ${days_sample}
############################################################
version=version10
softVesion=V10
jarPackage=./jar/TopicFeatureGenerator-1.0-SNAPSHOT-jar-with-dependencies.jar
static_user_behaviors=com.home.recommendation.features.FeatureAnalyse.static_user_behaviors
feeds_o2o_mifeeds_log_info=/user/s_lcs/feeds/feeds_o2o_mifeeds_log_info/year=${yesterday_year}/month=${yesterday_month}/day=${yesterday_day}
browser_comment_user_log=/user/s_lcs/browser/browser_comment_user_log/year=${yesterday_year}/month=${yesterday_month}/day=${yesterday_day}
output_hive_topic_deviceId_commentId_action=/user/h_data_platform/platform/browser/topicuserinterestedcategory/date=${day_today}
output_hdfs_topic_deviceId_commentId_action=/user/h_browser/algo/yuanzhijie/rec_system/recall/userInterest/static_user_behaviors_${version}/${day_now}
local_topic_deviceId_commentId_action=./data/static_user_behaviors_${version}_${day_now}

hadoop=/home/work/infra-client/bin/hadoop
function hadoop_file_exist_test(){
    ${hadoop} --cluster zjyprc-hadoop fs -test -e $1
    if [ $? -eq 0 ] ;then
        echo '++++++' $1 'exist' '++++++'
    else
        echo '------' $1 "dose not exist!!!" '------'
        exit 1
    fi
}
function file_exist(){
    hadoop_file_exist_test ${feeds_o2o_mifeeds_log_info}
    hadoop_file_exist_test ${browser_comment_user_log}
}
file_exist

for i in $(seq 1 ${days_sample})
do
    #echo $i
    date=`date +%Y%m%d  -d "${day_today} -$i days"`
    year=`date     -d "$date" +"%Y"`
    month=`date    -d "$date" +"%m"`
    day=`date      -d "$date" +"%d"`
    temp_file=/user/s_lcs/feeds/feeds_o2o_mifeeds_log_info/year=${year}/month=${month}/day=${day}
    feeds_o2o_mifeeds_log_info=${feeds_o2o_mifeeds_log_info},${temp_file}
done

days_before=30
for i in $(seq 1 $(( days_sample + days_before )))
do
    #echo $i
    date=`date +%Y%m%d  -d "${yesterday} -$i days"`
    year=`date     -d "$date" +"%Y"`
    month=`date    -d "$date" +"%m"`
    day=`date      -d "$date" +"%d"`
    temp_file=/user/s_lcs/browser/browser_comment_user_log/year=${year}/month=${month}/day=${day}
    browser_comment_user_log=${browser_comment_user_log},${temp_file}
done

echo "jarPackage=====================================: " ${jarPackage}
echo "static_user_behaviors==========================: " ${static_user_behaviors}
echo "feeds_o2o_mifeeds_log_info=====================: " ${feeds_o2o_mifeeds_log_info}
echo "browser_comment_user_log=======================: " ${browser_comment_user_log}
echo "output_hive_topic_deviceId_commentId_action====: " ${output_hive_topic_deviceId_commentId_action}
echo "output_hdfs_topic_deviceId_commentId_action====: " ${output_hdfs_topic_deviceId_commentId_action}
echo "local_topic_deviceId_commentId_action==========: " ${local_topic_deviceId_commentId_action}

export CLUSTER_NAME=zjyprc-hadoop
export queue=production.miui_group.browser.miui_browser_zjy_1
function spark_static_user_behaviors() {
    ${hadoop} --cluster ${CLUSTER_NAME} fs -rm -r ${output_hive_topic_deviceId_commentId_action}
    ${hadoop} --cluster ${CLUSTER_NAME} fs -rm -r ${output_hdfs_topic_deviceId_commentId_action}
    /home/work/infra-client/bin/spark-submit \
    --cluster ${CLUSTER_NAME} \
    --java 8 \
    --conf spark.yarn.appMasterEnv.JAVA_HOME=/opt/soft/openjdk1.8.0 \
    --conf spark.executorEnv.JAVA_HOME=/opt/soft/openjdk1.8.0 \
    --conf spark.yarn.job.owners=yuanzhijie \
    --conf fs.hdfs.impl.disable.cache=true \
    --conf spark.akka.frameSize=256 \
    --conf spark.yarn.alert.phone.number=13811828421 \
    --conf spark.yarn.alert.mail.address=yuanzhijie \
    --class ${static_user_behaviors} \
    --master yarn-cluster \
    --queue ${queue} \
    --driver-memory 12g \
    --num-executors 120 \
    --executor-memory 12g \
    --executor-cores 4 \
    ${jarPackage} ${feeds_o2o_mifeeds_log_info} ${browser_comment_user_log} ${output_hive_topic_deviceId_commentId_action} ${output_hdfs_topic_deviceId_commentId_action}
}

if [ $? == 0 ]
then
    echo "generator history behavior of the users"
    spark_static_user_behaviors
    if [[ $? != 0 ]]; then
        echo "something wrong to generator history behavior of the users"
        exit 1
    fi
    ${hadoop} --cluster ${CLUSTER_NAME} fs -getmerge ${output_hdfs_topic_deviceId_commentId_action} ${local_topic_deviceId_commentId_action}
fi
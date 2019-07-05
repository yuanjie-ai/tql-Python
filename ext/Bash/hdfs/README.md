- hdfs download
```bash
echo hdfs_path: $1
local_path=/home/work/yuanjie/all_data.tsv
hdfs --cluster zjyprc-hadoop dfs -getmerge $1 $local_path
du -sBG $local_path
```
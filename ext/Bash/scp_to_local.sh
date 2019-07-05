#!/usr/bin/env bash
echo "远程路径：$1"
echo "scp -r $1 yuanjie@10.234.196.9:/home/yuanjie/desktop/scp_work"
echo $line
scp -r $1 yuanjie@10.234.196.9:/home/yuanjie/desktop/scp_work

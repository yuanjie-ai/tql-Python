#!/usr/bin/env bash
echo "远程路径：$1"
echo "scp -r yuanjie@10.234.196.9:/home/yuanjie/desktop/scp_work $1"
echo $line

scp -r yuanjie@10.234.196.9:/home/yuanjie/desktop/scp_work $1

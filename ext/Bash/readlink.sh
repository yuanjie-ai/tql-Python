#!/usr/bin/env bash
PATH1=$(dirname $0) # 当前脚本相对路径
PATH2=$(cd `dirname $0`;pwd) # 当前脚本绝对路径
PATH3=$(readlink -f $PATH1/..) # 当前脚本绝对路径上一层
cur_path=$(readlink -f $(dirname "$0")) # 当前脚本路径


#path.sh
##!/bin/bash
#PATH1=$(dirname $0)
#PATH2=$(cd `dirname $0`;pwd)
#PATH3=$(readlink -f $PATH1/..)
#echo $PATH1
#echo $PATH2
#echo $PATH3
#当前脚本存在路径：/home/software
#sh path.sh
#.              【echo $PATH1】
#/home/software 【echo $PATH2】
#/home          【echo $PATH3】

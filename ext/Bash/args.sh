#!/bin/bash

echo "Shell 输出脚本名称及参数";
echo "执行的脚本名：$0";
echo "第一个参数为：$1";
echo "第二个参数为：$2";
echo "第三个参数为：$3";
echo $#;
echo $@;
echo $?;
echo $*;

while getopts ":a:b:c:" opt
do
    case $opt in
        a)
	export x=$OPTARG
        echo "参数a的值$OPTARG";;
        b)
        echo "参数b的值$OPTARG";;
        c)
        echo "参数c的值$OPTARG";;
        ?)
        echo "未知参数"
        exit 1;;
    esac
done


echo x

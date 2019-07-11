#!/usr/bin/env bash
#while getopts ":m:b:c:" opts
#do
#    case $opts in
#        m)
#        update_info=$OPTARG;;
#        b)
#        echo "参数b的值$OPTARG"≤;;
#        c)
#        echo "参数c的值$OPTARG";;
#        ?)
#        echo "未知参数"
#        exit 1;;
#    esac
#done

if [ -n "$1" ]
then update_info=$1
else update_info='update'
fi;
git pull
git add *
git commit -m $update_info
git push
pip uninstall tql -y \
&& pip install -U -i https://pypi.tuna.tsinghua.edu.cn/simple \
git+https://github.com/Jie-Yuan/tql-Python.git
exit 0
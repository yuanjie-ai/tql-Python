#!/usr/bin/env bash
# @Project      : tql-Python
# @Time         : 2019-07-24 17:42
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : ${DESCRIPTION}


# 编译安装http://www.zhangc.cn/?id=94
sed -i 's/python/python2.7/g' /usr/bin/yum # yum 只支持python2.7
yum -y install epel-release
yum -y install https://centos7.iuscommunity.org/ius-release.rpm
yum -y install python36u python36u-devel python36u-pip
ln -sf /usr/bin/pip3.6 /usr/bin/pip
ln -sf /usr/bin/python3.6 /usr/bin/python
chmod 777 /home/work
whereis pip
whereis python



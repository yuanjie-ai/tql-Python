#!/usr/bin/env bash
# @Project      : tql-Python
# @Time         : 2019-06-27 15:54
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : ${DESCRIPTION}
wget https://cmake.org/files/v3.15/cmake-3.15.0-rc2.tar.gz
tar -xvf cmake-3.15.0-rc2.tar.gz
cd ./cmake-3.15.0-rc2/
./configure
sudo make && make install

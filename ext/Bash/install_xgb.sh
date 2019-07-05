#!/usr/bin/env bash
# git@v9.git.n.xiaomi.com:yuanjie/xgboost.git
pip uninstall xgboost -y
git clone --recursive https://github.com/dmlc/xgboost; cd xgboost
mkdir build; cd build
cmake .. -DUSE_CUDA=ON
make -j4
cd ../python-package
python setup.py install


# 多gpu: https://www.cnblogs.com/kdyi/p/10636988.html
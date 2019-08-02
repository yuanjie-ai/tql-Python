#!/usr/bin/env bash
# @Project      : tql-Python
# @Time         : 2019-07-19 18:30
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : ${DESCRIPTION}

pip install -U -i https://pypi.tuna.tsinghua.edu.cn/simple black blackcellmagic
pip install blackcellmagic

# 在jupyter中添加命令
# %load_ext blackcellmagic
# %%black
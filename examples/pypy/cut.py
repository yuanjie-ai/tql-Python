#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : cut
# @Time         : 2019-08-27 13:49
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

import time
import jieba
from tqdm import tqdm

jieba.initialize()
s = "回过来再读取写入的文件，忽略函数 DictReader() 调用的参数 fieldnames，把第一行的值 （first,last）作为列标签，和字典的键做匹配"

start = time.time()
for i in tqdm([s] * 10000):
    jieba.lcut(i)

print(f"Use Time: {time.time() - start}")

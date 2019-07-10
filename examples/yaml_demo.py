#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : yaml
# @Time         : 2019-07-10 14:51
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

from pprint import pprint
import yaml
"""
https://www.cnblogs.com/klb561/p/9326677.html
https://blog.csdn.net/zhusongziye/article/details/80024426
"""

# dic = yaml.safe_load(open('yaml.yaml'))

# for k, v in dic.items():
#     print(k, ":", type(v).__name__, ':', v)


dic = yaml.safe_load(open('yaml_demo.yaml'))

pprint(dic)
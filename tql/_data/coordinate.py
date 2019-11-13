#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : coordinate
# @Time         : 2019-09-22 16:00
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

import re
import requests

url = 'https://blog.csdn.net/Yellow_python/article/details/81115987'
header = {'User-Agent': 'Opera/8.0 (Windows NT 5.1; U; en)'}
r = requests.get(url, headers=header)
contain = re.findall('<pre><code>([\s\S]+?)</code></pre>', r.text)[0].strip()
with open('coordinate.txt', 'w', encoding='utf-8') as f:
    f.write(contain)

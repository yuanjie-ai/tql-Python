#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : weather
# @Time         : 2020/8/24 9:01 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


import time
import json

import requests


def get_data(year='2020', month='08'):
    url = f'http://d1.weather.com.cn/calendar_new/{year}/101010100_{year}{month}.html?_={int(time.time())}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36',
        'Referer': 'http://www.weather.com.cn/weather40d/101010100.shtml'
    }
    r = requests.get(url, headers=headers)
    return json.loads(r.content[11:])  # pd.DataFrame(data)

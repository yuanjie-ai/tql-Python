#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'demo'
__author__ = 'JieYuan'
__mtime__ = '2019-04-30'
"""

import requests


def request(url, params=None):
    try:
        # headers：伪装spider
        headers = {'user-agent': 'Mozilla/5.0'}
        r = requests.get(url, params, headers=headers)
        r.raise_for_status()  # 申请返回的状态码: 200为成功
        r.encoding = r.apparent_encoding
        print(r.text.split()[:32])
        return r

    except Exception as e:
        print('爬取失败：%s' % e)


if __name__ == '__main__':
    request('https://www.baidu.com/s?wd=周杰伦')
    request('https://www.baidu.com/s', {'wd': '周杰伦'})

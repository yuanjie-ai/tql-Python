#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
__title__ = 'proxies'
__author__ = 'JieYuan'
__mtime__ = '2019-05-15'
"""
import requests
import pandas as pd
from tqdm import tqdm


class Proxies(object):

    def __init__(self, ):
        url = 'https://www.xicidaili.com/nn/'
        r = requests.get(url, headers={'user-agent': 'Mozilla/5.0'})
        self.ips = pd.read_html(r.text, header=0)[0][['IP地址', '端口']].values

    @property
    def pool(self):
        proxies = []
        for i in tqdm(self.ips):
            proxy = self._get_valid_proxies(i)
            if proxy:
                proxies.append(proxy)
        return proxies

    def _get_valid_proxies(self, ip):
        try:
            requests.adapters.DEFAULT_RETRIES = 3
            host, port = ip  # random.choice(ips)
            proxies = {"http": "http://%s:%s" % (host, port)}
            r = requests.get("http://icanhazip.com/", timeout=8, proxies=proxies)
            if host == r.text.strip():
                # print('代理有效：%s' % proxies)
                return proxies
            else:
                print("pass")  # 代理无效
        except:
            print("pass")


if __name__ == '__main__':
    pool = Proxies().pool
    print(pool)
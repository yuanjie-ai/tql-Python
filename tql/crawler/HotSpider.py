#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'HotSpider'
__author__ = 'JieYuan'
__mtime__ = '2019-05-15'
"""
from ..pipe import tqdm

import requests
import pandas as pd
from lxml.etree import HTML
from fake_useragent import UserAgent


class HotSpider(object):

    def __init__(self, query='news'):
        """

        :param query:
        :param categories:
        """
        self.query = query
        self.categories = ['news', 'tech', 'ent', 'shopping', 'community']
        self.ua = UserAgent()

    def df_sites_info(self):
        self.urls = self.df_sites.url

        dfs = []
        for url in tqdm(self.urls):
            r = self._request(url)
            dom_tree = HTML(r.text)
            site = dom_tree.xpath('normalize-space(//div[@class="Xc-ec-L b-L"]/text())')
            print('🕷：%s %s' % (site, url))

            df = pd.read_html(self._request(url).text)[0]
            df.columns = ['rank', 'title', 'hot', 'site']
            df['site'] = site
            df['url'] = url
            dfs.append(df)
        return pd.concat(dfs)  # pd.merge(self.df_sites, pd.concat(dfs))

    @property
    def df_sites(self):
        print('🕷：%s ...' % self.query)
        if self.query in self.categories:
            url = 'https://tophub.today/c/' + self.query
            r = self._request(url)
            dom_tree = HTML(r.text)
            pages = int(dom_tree.xpath('//div/small/text()')[0][:-1]) // 12 + 1
            urls = [url + '?p=%s' % i for i in range(1, pages + 1)]
            print('%s: %s' % (self.query, pages))
        else:
            urls = ['https://tophub.today/search?q=' + self.query]

        dfs = []
        for url in urls:
            r = self._request(url)
            dom_tree = HTML(r.text)
            urls = dom_tree.xpath('//div/a[starts-with(@href,"/n")]/@href')
            subscriber_num = dom_tree.xpath('//span[@class="zb-Rb-subscriber-Wc"]/text()')

            df_sites = pd.DataFrame()
            df_sites['url'] = ['https://tophub.today' + i for i in urls]
            df_sites['subscriber_num'] = pd.Series(subscriber_num).astype(int)
            df_sites.sort_values('subscriber_num', 0, False, True)
            dfs.append(df_sites)
        return pd.concat(dfs)

    @property
    def headers(self):
        return {'user-agent': self.ua.random}

    def _request(self, url):
        try:
            r = requests.get(url, timeout=500, headers=self.headers)
            r.raise_for_status()
            r.encoding = 'utf8'  # r.apparent_encoding
            return r

        except Exception as e:
            print('🕷：%s' % e)

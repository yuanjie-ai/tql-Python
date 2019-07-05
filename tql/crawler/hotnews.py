#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'topnews'
__author__ = 'JieYuan'
__mtime__ = '2019-05-07'
"""
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup


class HotNews(object):

    def __init__(self):
        pass

    def tuling(self, q):
        url = 'http://www.tuling123.com/openapi/api?key=3ac26126997942458c0d93de30d52212&info='
        return requests.get(url + q).json()['text']

    def sina(self):
        url = 'http://www.sina.com.cn/mid/search-list.shtml'
        soup = self._get_soup(url)
        soups = soup.findAll('div', re.compile('keyword|exp'))

        news = []
        for idx in range(0, len(soups), 2):
            s1 = soups[idx].text.split(r'#')[1]
            s2 = soups[idx + 1].text
            news.append([s1, s2])

        return news

    def weibo(self):
        url = 'https://s.weibo.com/top/summary?cate=realtimehot'
        # df = pd.read_html(url)[0][['关键词']]
        soup = self._get_soup(url)
        soups = soup.findAll(re.compile('td|span'), 'td-02')

        news = []
        for s in soups:
            s1 = s.a.text
            s2 = s.span.text if s.span else ''
            news.append([s1, s2])
        return news

    def baidu(self, period=0):
        _map = {0: 1, 1: 341, 7: 42}
        url = 'http://top.baidu.com/buzz?b=%s' % _map.get(period, _map[0])

        df = pd.read_html(url, header=0)[0].dropna().drop(['排名', '相关链接'], 1)
        return df

    def sougou(self, period=0):
        _map = {0: 'shishi', 7: 'sevendsnews'}

        news = []
        for i in range(3):
            url = 'http://top.sogou.com/hot/%s_%s.html' % (_map.get(period, _map[0]), i + 1)
            soup = self._get_soup(url)

            soups = soup.findAll(re.compile('span|p'), re.compile('s3|p1|p3'))
            for idx in range(0, len(soups), 2):
                s1 = soups[idx].text
                s2 = soups[idx + 1].text
                s3 = soups[idx + 1].find().attrs['class'][0]
                news.append([s1, s2, s3])
        return news

    def qihu(self, period=0):
        _map = {0: 'https://news.so.com/hotnews',
                1: 'https://trends.so.com/top/realtime'}
        url = _map.get(period, _map[1])

        if period:
            r = requests.get(url, timeout=300, headers={'user-agent': 'Mozilla/5.0'})
            r.encoding = r.apparent_encoding
            return pd.DataFrame(r.json()['data']['result'])
        else:
            soup = self._get_soup(url)

            news = []
            soups = soup.findAll('span', class_=re.compile('title|hot'))
            for idx in range(0, len(soups), 2):
                s1 = soups[idx].string
                s2 = soups[idx + 1].string
                news.append([s1, s2])
            return news

    def _get_soup(self, url='https://www.baidu.com'):
        try:
            r = requests.get(url, timeout=300, headers={'user-agent': 'Mozilla/5.0'})
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            return BeautifulSoup(r.text)
        except:
            print('爬取失败')



if __name__ == '__main__':
    hn = HotNews()
    print(pd.DataFrame(hn.sina()))

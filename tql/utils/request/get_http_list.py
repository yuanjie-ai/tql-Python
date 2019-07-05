#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
__title__ = 'get_http_list'
__author__ = 'JieYuan'
__mtime__ = '19-3-12'
"""

def get_http_list(url="http://10.114.38.22:9999"):
    import requests
    from bs4 import BeautifulSoup
    soup=BeautifulSoup(requests.get(url).text, "lxml") # soup.prettify()
    # soup.find_all('div', class_='cangtoushi-item')
    print(soup.text)
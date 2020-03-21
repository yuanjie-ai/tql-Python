#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : main
# @Time         : 2020-01-10 16:37
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

import httpx
import requests
from lxml.etree import HTML


class Poem(object):

    def __init__(self):
        pass

    def p1(self, title):
        url = f"http://www.guabu.com/cangtoushi/?type=guabu&key={title}&leixing=1&len=7"
        dom_tree = self.get_html(url)
        return dom_tree.xpath('//*[@id="summary"]/div//text()')

    def p2(self, title):
        url = f"http://www.shicimingju.com/cangtoushi/index.html?kw={title}&zishu=7&position=0"
        dom_tree = self.get_html(url)
        _ = dom_tree.xpath('//div[@class="card"]/text()')
        return ''.join(_).split()[:len(title)]

    @staticmethod
    def get_html(url):
        r = requests.get(url, timeout=10)
        dom_tree = HTML(r.text)
        return dom_tree


if __name__ == '__main__':
    a = Poem().p1("新年快乐")
    print(a)

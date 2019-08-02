#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : restful_sanic
# @Time         : 2019-07-18 10:13
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


import jieba
from restful_api import Api
import requests

from lxml.etree import HTML
from googletrans import Translator

translator = Translator(service_urls=['translate.google.cn', 'translate.google.com'],
                        timeout=3)


def trans_google(q='苹果', fromLang='auto', toLang='en'):
    """

    :param q:
    :param fromLang:
    :param toLang: zh
    :return:
    """
    url = "http://translate.google.cn/translate_a/single?client=gtx&dt=t&dj=1&ie=UTF-8&sl=%s&tl=%s" % (fromLang, toLang)
    try:
        r = requests.get(url, {'q': q}, timeout=3)
        text = r.json()['sentences'][0]['trans']
    except Exception as e:
        print(e)
        text = translator.translate(q, toLang, fromLang).text
    return text


def get_title(url='https://baijiahao.baidu.com/s?id=1604534610481479105&wfr=spider&for=pc&isFailFlag=1'):
    r = requests.get(url, headers={'user-agent': 'Mozilla/5.0'})
    r.encoding = r.apparent_encoding
    # soup = BeautifulSoup(r.text)
    dom_tree = HTML(r.text)
    title = dom_tree.xpath('//title/text()')
    return title[0]


api = Api('/ctr/trans', trans_google, method='GET', verbose=False)
api = Api('/get_title', get_title, api.app)

api.app.run('0.0.0.0')

# import requests
# json = {'x': 1, 'y': 10}
# requests.post('http://127.0.0.1:8000/post1', json=json).json()
# requests.post('http://127.0.0.1:8000/post2', json=json).json()
# requests.post('http://127.0.0.1:8000/post3', json=json).json()

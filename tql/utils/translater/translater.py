#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'translate'
__author__ = 'JieYuan'
__mtime__ = '19-3-1'
"""
import requests
import random
import hashlib

"""可以通过docker增加并发
https://www.cnblogs.com/fanyang1/p/9414088.html
https://github.com/ssut/py-googletrans

https://github.com/openlabs/Microsoft-Translator-Python-API
https://github.com/cognitect/transit-python
"""
from .tencent import trans_tencent
from googletrans import Translator
from .youdao import trans_youdao

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


def trans_baidu(q='苹果', fromLang='auto', toLang='en'):
    """

    :param q:
    :param fromLang:
    :param toLang: zh简体 en英文
    :return:
    """
    url = "http://api.fanyi.baidu.com/api/trans/vip/translate"
    appid = '20190718000319131'  # 你的appid
    secretKey = 'goP6CsXs6sVamHtRGdBa'  # 你的密钥
    salt = str(random.randint(32768, 65536))
    # 生成签名
    sign = appid + q + salt + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    data = {
        "appid": appid,
        "q": q,
        "from": fromLang,
        "to": toLang,
        "salt": salt,
        "sign": sign,
    }
    r = requests.post(url, data=data, timeout=3)
    return r.json().get('trans_result')[0].get("dst")


if __name__ == '__main__':
    print(trans_tencent())
    print(trans_google('apple', 'en', 'zh'))
    print(trans_baidu('apple', 'en', 'zh'))

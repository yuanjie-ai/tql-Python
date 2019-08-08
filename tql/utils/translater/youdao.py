#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : youdao
# @Time         : 2019-08-07 13:21
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :
import time

import requests
import hashlib


def trans_youdao(q="苹果", fromLang='auto', toLang='en'):
    t = str(int(time.time()))
    c = "rY0D^0'nM0}g5Mm1z%1G4"
    u = 'fanyideskweb'
    creatmd5 = u + q + t + c

    # 生成md5
    md5 = hashlib.md5()
    md5.update(creatmd5.encode('utf-8'))
    sign = md5.hexdigest()

    data = {}
    data['i'] = q
    data['from'] = fromLang
    data['to'] = toLang
    data['smartresult'] = 'dict'
    data['client'] = 'fanyideskweb'
    data['salt'] = t
    data['sign'] = sign
    data['doctype'] = 'json'
    data['version'] = '2.1'
    data['keyfrom'] = 'fanyi.web'
    data['action'] = 'FY_BY_CLICKBUTTION'
    data['typoResult'] = 'true'

    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&sessionFrom='
    return requests.post(url, data).json()['translateResult']


if __name__ == '__main__':
    print(trans_tencent('apple', toLang="zh"))
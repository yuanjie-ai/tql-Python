#!/usr/bin/env bash
# @Project      : tql-Python
# @Time         : 2019-11-28 11:49
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : siege -c 500 r -1  'HTTP_URL POST <./postfile.json'

#siege -c 10 -r 1000 'http://web.algo.browser.miui.srv/nlp/wv POST <./post.json' \
#> request.txt

siege -c 10 -r 10000 'http://web.algo.browser.miui.srv/poetry/藏头诗' \
>> request.txt

#Transaction rate:	      208.65 trans/sec

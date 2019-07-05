#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : iWork.
# @File         : demo
# @Time         : 2019-06-14 16:46
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


from selenium import webdriver

options = webdriver.ChromeOptions()
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-extensions')
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')
# options.add_argument('blink-settings=imagesEnabled=false')
# options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"')
options.add_argument("--proxy-server=http://proxy.pt.xiaomi.com:80")

driver = webdriver.Chrome(options=options)
url = "http://zjy-hadoop-prc-ct12.bj:20701"
driver.get(url)
# driver.implicitly_wait(10)

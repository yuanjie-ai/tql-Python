#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : iWork.
# @File         : demo
# @Time         : 2019-06-14 16:46
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

# TODO: 爬虫服务
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
# driver.page_source
# driver.implicitly_wait(10)


# url = "https://m.weibo.cn/"
# driver.get(url)
# d = driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[1]/div[2]/div/div[1]/div/div/ul/li[9]/span')
#
# d.click()
# from lxml.etree import HTML
# dom_tree = HTML(driver.page_source)
# title = dom_tree.xpath('//div[@class="weibo-text"]//text()')

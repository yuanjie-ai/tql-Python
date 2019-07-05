#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'download_file'
__author__ = 'JieYuan'
__mtime__ = '18-12-27'
"""
import pickle
import requests
from tqdm import tqdm
from sklearn.externals import joblib


class DownloadFile(object):
    """方便远程部署模型"""

    def get(self, url, mode='sklearn'):
        self.__get_file(url)
        if mode == 'sklearn':
            obj = joblib.load('./temp.txt')
        elif mode == 'pickle':
            with open('./temp.txt', 'rb') as f:
                obj = pickle.load(f)
        else:
            print("please read with open('./temp.txt') !!!")
            obj = "./temp.txt"
        return obj

    def __get_file(self, url, tempfile='./temp.txt'):
        try:
            res = requests.get(url)
            res.raise_for_status()
            with open(tempfile, 'wb') as f:
                for lines in tqdm(res.iter_content(100000), 'Loading'):
                    f.write(lines)
        except:
            print('please input correct url !!!')

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : data
# @Time         : 2020-01-14 13:12
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

import re

reg_chinese = re.compile('[^a-zA-Z\u4e00-\u9fa5]+')

text = '沈萌表示，中石化入股九州证券一方面可以将触角伸向证券业，另一方面也可以未来的混合所有制改革等与金融服努机构建立更深入的合作关系'
entity = '沈萌，PER;中石化，COM;九州证券，COM;'  # B-PER I-PER 其他为O

print(reg_chinese.split(entity))

# entity_map = {'沈萌': 'PER',
#     '中石化': 'COM',
#     '九州证券': 'COM'
# }

entity_map = [('沈萌', 'PER'), ('中石化', 'COM'), ('九州证券', 'COM')]

for char in zip(text, 'O' * len(text)):
    if char in '沈萌' or char in '中石化' or char in '九州证券':
        print(char)

# word = '沈萌'
# new = ['B-PER'] + ['I-PER']*(len(word) - 1)
# print(text.replace(word, ' '.join(new)))
# 不置信 自动化试探 提前减量



if __name__ == '__main__':
    pass

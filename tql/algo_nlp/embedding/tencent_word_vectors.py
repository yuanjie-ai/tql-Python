#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'tencent_word_vectors'
__author__ = 'JieYuan'
__mtime__ = '19-2-13'
"""
import numpy as np
from tqdm import tqdm

fname = '/home/yuanjie/desktop/data/Tencent_AILab_ChineseEmbedding/Tencent_AILab_ChineseEmbedding.txt'
idf = {}
with open(fname) as f:
    for line in tqdm(f, 'Load Vectors ...'):
        line = line.strip().split()
        if len(line) > 2:
            idf[line[0]] = np.linalg.norm(np.asarray(line[-200:], dtype='float32'), 2)

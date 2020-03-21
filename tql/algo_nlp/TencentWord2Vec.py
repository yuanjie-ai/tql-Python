# -*- coding: utf-8 -*-

"""
__title__ = 'twv'
__author__ = 'JieYuan'
__mtime__ = '18-11-13'
"""

from tqdm import tqdm
import pymongo

from concurrent.futures import ThreadPoolExecutor
from scipy.spatial.distance import pdist

from sklearn.metrics.pairwise import cosine_similarity

class TencentWord2Vec(object):

    def __init__(self):
        self.db = pymongo.MongoClient().ChineseEmbedding.TencentWord2Vec

    def __getitem__(self, items):
        if isinstance(items, str):
            return self.get_vector([items])[0]
        else:
            return self.get_vector(items)

    def cosine(self, w1, w2):
        return 1 - pdist(self.get_vector((w1, w2)), 'cosine')[0]

    def get_vector(self, words):
        """
        from sklearn.metrics.pairwise import cosine_similarity
        >>> a=[[1,3,2],[2,2,1]]
        >>> cosine_similarity(a)
        """
        with ThreadPoolExecutor(8 if len(words) > 8 else len(words)) as pool:
            vecs = pool.map(self.__func, words)
        return list(vecs)

    def __insert_word2vec(self):

        self.db.delete_many({})
        for line in self.__reader():
            _ = self.db.insert_one(line)

    def __func(self, word):
        return self.db.find_one({'word': word})['vector']

    def __reader(self):
        with open("/home/yuanjie/下载/Tencent_AILab_ChineseEmbedding/Tencent_AILab_ChineseEmbedding.txt") as f:
            for idx, line in tqdm(enumerate(f), 'Loading ...'):
                ws = line.strip().split(' ')
                if idx:
                    yield {'word': ws[0], 'vector': [float(i) for i in ws[1:]]}

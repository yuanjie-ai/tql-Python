#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'Doc2Vec'
__author__ = 'JieYuan'
__mtime__ = '2019-05-23'
"""
from tqdm import tqdm
from pathlib import Path
from gensim.models.doc2vec import Doc2Vec, TaggedDocument, TaggedLineDocument


class GensimDoc2Vec(object):
    def __init__(self):
        pass

    def fit(self, corpus, vector_size=300, window=10, min_count=1, dm=1, hs=0, negative=5,
            epochs=10, workers=8):

        if isinstance(corpus, str) and Path(corpus).is_file():
            corpus = TaggedLineDocument(corpus)
        else:
            corpus = [TaggedDocument(line, [idx]) for idx, line in enumerate(corpus)]

        model = Doc2Vec(documents=tqdm(corpus), vector_size=vector_size,
                        window=window, min_count=min_count, dm=dm,
                        hs=hs, negative=negative, epochs=epochs, workers=workers)
        return model


if __name__ == '__main__':
    docs = [['Well', 'done!'],
            ['Good', 'work'],
            ['Great', 'effort'],
            ['nice', 'work'],
            ['Excellent!'],
            ['Weak'],
            ['Poor', 'effort!'],
            ['not', 'good'],
            ['poor', 'work'],
            ['Could', 'have', 'done', 'better.']]
    model = GensimDoc2Vec()
    model.fit(docs)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : TextClean
# @Time         : 2019-06-21 18:19
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

from ...pipe import get_module_path

import jieba.posseg as jp


# TODO: 统计特征、emoji


class TextClean(object):

    def __init__(self):
        self._stopwords = self._get_stopwords()

    # def get_words(self, sent, flags=None):
    #     """
    #     :flags mode: ['v', 'vn']
    #     """
    #     for p in jp.cut(sent.lower()):
    #         if p.flag in flags:
    #             yield p.word

    def get_noun(self, doc, with_flag=False):
        for p in jp.cut(doc.lower()):
            if p.word not in self._stopwords:
                if 'n' in p.flag and len(p.word) > 1:  # 长度大于1且非停顿词的名词
                    yield p if with_flag else p.word

    def _get_stopwords(self):
        with open(get_module_path('../../_data/stop_words.txt', __file__), encoding='utf8') as f:
            return set(f.read().split())

    def is_noun(w='潮玩'):
        for p in jp.lcut(w):
            if 'n' in p.flag:
                return True

# def remove_special_characters(text):
#     tokens = tokenize_text(text)
#     pattern = re.compile('[{}]'.format(re.escape(string.punctuation)))
#     filtered_tokens = filter(None, [re.sub(pattern=pattern, repl="", string=token) for token in tokens])
#     filtered_text = ''.join(filtered_tokens)
#     return filtered_text
#
#
# def normalize_corpus(corpus):
#     normalized_corpus = []
#     for text in corpus:
#         text = remove_special_characters(text)
#         text = remove_stopwords(text)
#         normalized_corpus.append(text)
#     return normalized_corpus

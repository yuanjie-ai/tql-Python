#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'check_coverage'
__author__ = 'JieYuan'
__mtime__ = '19-1-31'
"""

# from gensim.models import KeyedVectors
#
# news_path = '../input/embeddings/GoogleNews-vectors-negative300/GoogleNews-vectors-negative300.bin'
# embeddings_index = KeyedVectors.load_word2vec_format(news_path, binary=True)
#
# import operator
#
#
# def check_coverage(vocab, embeddings_index):
#     a = {}
#     oov = {}
#     k = 0
#     i = 0
#     for word in tqdm(vocab):
#         try:
#             a[word] = embeddings_index[word]
#             k += vocab[word]
#         except:
#
#             oov[word] = vocab[word]
#             i += vocab[word]
#             pass
#
#     print('Found embeddings for {:.2%} of vocab'.format(len(a) / len(vocab)))
#     print('Found embeddings for  {:.2%} of all text'.format(k / (k + i)))
#     sorted_x = sorted(oov.items(), key=operator.itemgetter(1))[::-1]
#
#     return sorted_x
#
#
# if __name__ == '__main__':
#     oov = check_coverage(vocab, embeddings_index)

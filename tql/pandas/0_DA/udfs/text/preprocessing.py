# coding: utf-8

import jieba
from snownlp import SnowNLP


def get_text_tokens(text, stop_words_path="./stop_words.txt"):
    text_tokens = jieba.cut(text.strip())
    stop_words = get_stop_words(stop_words_path)
    word_list = []
    for word in text_tokens:
        if word not in stop_words:
            if word != '\t':
                word_list.append(word)
    return word_list  # 词频Counter(word_list)


def get_stop_words(path="./stop_words.txt"):
    with open(path) as f:
        stop_words = [line.strip() for line in f.readlines()]
    return stop_words


def fan2jian(text):
    """
    :param text:
    :return: 繁体转简体
    """
    return SnowNLP(text).han


def get_pinyin(text):
    """
    :param text:
    :return: 汉字转拼音
    """
    return SnowNLP(text).pinyin

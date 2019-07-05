#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'emoji_feats'
__author__ = 'JieYuan'
__mtime__ = '2019/4/16'
"""

import emoji
from collections import Counter


class Emoji(object):

    def __init__(self):
        self.regexp = emoji.get_emoji_regexp()

    def counter(self, s="👍💝💝😁😁😁 言之有理", topk=None):
        c = Counter(self.regexp.findall(s))
        return c.most_common(topk)


if __name__ == '__main__':
    e = Emoji()
    print(e.counter())
    print(e.counter(topk=2))

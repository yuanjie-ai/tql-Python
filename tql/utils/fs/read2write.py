#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'read2write'
__author__ = 'JieYuan'
__mtime__ = '19-3-15'
"""

from tqdm import tqdm


def read2write(ifile, ofile, progress_func=lambda x: x, lower=True, overwrite=True):
    """pypy"""
    with open(ifile, 'r', encoding='utf8') as input, \
            open(ofile, 'w' if overwrite else 'a', encoding='utf8') as output:
        for line in tqdm(input):
        # for idx, line in enumerate(input):
        #     if idx % 100_000 == 0:
        #         print(idx)
            if line.strip():
                _ = progress_func(line.lower() if lower else line)
                output.write(_ + '\n')


if __name__ == '__main__':
    read2write('/Users/yuanjie/Desktop/notebook/0_MI/training/17/part-00000',
               '/Users/yuanjie/Desktop/notebook/0_MI/test.json',
               lambda x: str(eval(x)))





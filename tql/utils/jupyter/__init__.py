#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '__init__.py'
__author__ = 'JieYuan'
__mtime__ = '2019/4/2'
"""

import jovian


def commit(notebook_id=None, nb_filename=None):
    """
    sh： jovian clone notebook_id
    :param nb_filename:
    :param notebook_id: 内容覆盖566f95b138a9465aa8d17e0f1836570a -> https://jvn.io/Jie-Yuan/566f95b138a9465aa8d17e0f1836570a
    :return:
    """
    print(
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlkZW50aXR5Ijp7InVzZXJuYW1lIjoiSmllLVl1YW4iLCJpZCI6Njd9LCJ0eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTUyOTY1NTkzLCJpYXQiOjE1NTIzNjA3OTMsIm5iZiI6MTU1MjM2MDc5MywianRpIjoiNjM1ZTg2MjQtYjA1ZC00NGJmLTljYjAtOGVjOGRmM2ExNmJkIn0.5jglhEGGs12ITl-DWWaFL-BVPhCzaDEeMKIJvEI-bbA")
    print('\n')
    jovian.commit(nb_filename=nb_filename, env_type='pip', notebook_id=notebook_id)

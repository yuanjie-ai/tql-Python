#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : is_in_notebook
# @Time         : 2019-06-20 11:16
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


def _in_notebook():
    try:
        from IPython import get_ipython

        if 'IPKernelApp' not in get_ipython().config:
            raise ImportError("Not In Notebook !")
    except:
        return False

    else:
        return True


if __name__ == '__main__':
    print(_in_notebook())

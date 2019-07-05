# -*- coding: utf-8 -*-
"""
__title__ = 'Singleton'
__author__ = 'JieYuan'
__mtime__ = '2018/7/28'
"""
import functools
import inspect
import time
from collections import Iterable

import numpy as np
import wrapt
from tqdm import tqdm

"""定义装饰器"""


@wrapt.decorator
def pass_through(wrapped, instance, args, kwargs):
    return wrapped(*args, **kwargs)


def with_arguments(myarg1, myarg2):
    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        return wrapped(*args, **kwargs)

    return wrapper


@wrapt.decorator
def universal(wrapped, instance, args, kwargs):
    """
    class A:
        @universal
        def f(self, x):
            return x

    @universal
    def f(x):
        return x
    """
    if instance is None:
        if inspect.isclass(wrapped):
            print('Decorator was applied to a class.')
            return wrapped(*args, **kwargs)
        else:
            print('Decorator was applied to a function or staticmethod.')
            return wrapped(*args, **kwargs)
    else:
        if inspect.isclass(instance):
            print('Decorator was applied to a classmethod.')
            return wrapped(*args, **kwargs)
        else:
            print('Decorator was applied to an instancemethod.')
            return wrapped(*args, **kwargs)


##################################################################################

##################################################################################
def mytqdm(desc=None):
    def wrapper(func):
        @functools.wraps(func)
        def _wrapper(iter_obj, *args, **kwargs):
            """保证第一个参数为可迭代参数即可"""
            assert isinstance(iter_obj, Iterable)
            with tqdm(iter_obj, desc) as t:
                temp = func(t, *args, **kwargs)
            return temp

        return _wrapper

    return wrapper


"""类里调用增加self参数使得能够修饰类方法
def mytqdm(desc=None):
    def wrapper(func):
        @functools.wraps(func)
        def _wrapper(_self, iter_obj, *args, **kwargs):
            assert isinstance(iter_obj, Iterable)
            with tqdm(iter_obj, desc) as t:
                temp = func(_self, t, *args, **kwargs)
            return temp

        return _wrapper

    return wrapper
"""


##################################################################################
def feval(multiclass=None, is_bigger_better=True, model='lgb'):
    """example
    @feval(3)
    def f1_score(y_pred, y_true):
        '注意入参顺序'
        return f1_score(y_true, y_pred, average='macro')
    """

    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        y_pred, y_true = args
        y_true = y_true.get_label()
        if model == 'lgb':
            if multiclass:
                y_pred = np.array(y_pred).reshape(multiclass, -1).argmax(0)
            return wrapped.__name__, wrapped(y_pred, y_true), is_bigger_better
        elif is_bigger_better:
            """xgb评估指标默认越小越好"""
            return '-' + wrapped.__name__, - wrapped(y_pred, y_true)
        else:
            return wrapped.__name__, wrapped(y_pred, y_true)

    return wrapper


##################################################################################
@wrapt.decorator
def execution_time(wrapped, instance, args, kwargs):
    def call():
        start = time.time()
        tmp = wrapped(*args, **kwargs)
        print("""\nExecuting Time of "%s": %.3f s""" % (wrapped.__name__, time.time() - start))
        return tmp

    if instance is None:
        if inspect.isclass(wrapped):
            print('Decorator was applied to a class.')
            return call()
        else:
            print('Decorator was applied to a function or staticmethod.')
            return call()
    else:
        if inspect.isclass(instance):
            print('Decorator was applied to a classmethod.')
            return call()
        else:
            print('Decorator was applied to an instancemethod.')
            return call()


##################################################################################
class Singleton:
    def __init__(self, cls):
        self.cls = cls
        self.instance = None

    def __call__(self, *args, **kwargs):
        if self.instance is None:
            self.instance = self.cls(*args, **kwargs)
        return self.instance


def singleton(cls):
    """单例"""
    instances = {}

    def getinstance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return getinstance

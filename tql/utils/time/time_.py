# -*- coding: utf-8 -*-
"""
__title__ = 'time_utils'
__author__ = 'JieYuan'
__mtime__ = '2018/7/27'
"""
import time
import numpy as np

# pd.datetime.now().timestamp() # pd.datetime.now(cst_tz).timestamp()# 时间戳相差8*3600
# pd.read_csv(parse_dates)


# 时间戳 转 时间字符串
def timestamp2str(timestamp, format=''):
    """
    t = pd.datetime.now().timestamp()
    ts = pd.Series([t]*10, name='t')

    # 时间戳 转 时间字符串
    ts = ts.map(timestamp2str) # 会有时区问题 %Y-%m-%d %H:%M:%S
    # 时间字符串 转 时间
    ts = ts.astype('datetime64[ns]') # 慢一些 pd.to_datetime(ts, errors='coerce', infer_datetime_format=True)

    # 时间 转 时间戳
    ts.map(lambda x: x.timestamp())

    """
    return time.strftime(format, time.localtime(timestamp))


def exponential_decay(t, delta=24 * 7, start=1, end=0):
    """
    "拟合随时间指数衰减的过程"
    https://blog.csdn.net/xiaokang06/article/details/78076925
    https://blog.csdn.net/zhufenghao/article/details/80879260

    """
    alpha = np.log(start / (end + 1e-8)) / delta
    t0 = - np.log(start) / alpha

    decay = np.exp(-alpha * (t + t0))
    return decay

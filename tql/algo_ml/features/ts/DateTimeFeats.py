#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : iWork.
# @File         : DateTimeFeat
# @Time         : 2019-06-13 23:16
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 
import pandas as pd
from tqdm import tqdm
from datetime import timedelta

tqdm.pandas()


class DateTimeFeats(object):
    """
    pandas_utils 时间/日期特征工程
    常见格式：
        1. 时间戳
        2. 时间字符串

    # 很强大: 解析不出为空
    pd.to_datetime(ts, 'coerce', unit='s', infer_datetime_format=True)
    """

    def __init__(self, include_feats=None):
        """
        :param include_feats: 默认
            ("year", "quarter", "month", "day", "hour", "minute", "week", "weekday", "weekofyear")
            weekofyear == week?
            TODO: + "DayOfWeekInMonth": 当月第几周
            利用python获取某年中每个月的第一天和最后一天
        """
        self.time_granularity = ("year", "quarter", "month",
                                 "day", "hour", "minute",
                                 "week", "weekday", "weekofyear")

        self.feats = include_feats if include_feats else self.time_granularity

    def transform(self, s: pd.Series, add_prefix=None):
        if s.name is None:
            s.name = 'time_str'
        if add_prefix is None:
            add_prefix = f"{s.name}_"
        feats = self.feats

        _dtype = s.dtypes.__str__()
        if _dtype.__contains__('int') or _dtype.__contains__('float'):  # 时间戳 10位是秒 13位是毫秒
            print("infer_datetime_format: timestamp2date")
            ts = self.timestamp2date(s)
        else:
            print('infer_datetime_format: dateStr2date')
            ts = self.dateStr2date(s)

        _ = ts.progress_map(lambda t: list(self._func(t, feats)))
        df_ts = pd.DataFrame(_.tolist(), columns=feats).add_prefix(add_prefix)
        df_ts.insert(0, f'{s.name}2date', ts)
        return df_ts

    def _func(self, t, feats):
        for feat in feats:
            _ = t.__getattribute__(feat)
            if callable(_):
                yield _()
            else:
                yield _

    def timestamp2date(self, ts):
        return pd.to_datetime(ts, 'coerce', unit='s', infer_datetime_format=True)

    def dateStr2date(self, ts):
        try:
            _ = ts.astype('datetime64[ns]')
        except Exception as e:
            print("astype('datetime64[ns]'): %s" % e)
            _ = pd.to_datetime(ts, 'coerce', infer_datetime_format=True)
        return _

    def DayOfWeekInMonth(self, t):
        """
        获取指定的某天是某个月的第几周
        周一为一周的开始
        实现思路：就是计算当天在本年的第y周，本月一1号在本年的第x周，然后求差即可。
        """
        b = int((t - timedelta(t.day - 1)).strftime("%W"))
        e = int(t.strftime("%W"))
        return e - b + 1


if __name__ == '__main__':
    import pandas as pd

    ts = pd.Series([pd.datetime.today()] * 10)
    print(DateTimeFeats().transform(ts))

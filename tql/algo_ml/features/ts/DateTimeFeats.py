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

tqdm.pandas()


class DateTimeFeats(object):
    """
    pandas 时间/日期特征工程
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
        """
        self.time_granularity = ("year", "quarter", "month",
                                 "day", "hour", "minute",
                                 "week", "weekday", "weekofyear")

        self.feats = include_feats if include_feats else self.time_granularity

    def transform(self, s: pd.Series, add_prefix=None):
        if add_prefix is None:
            add_prefix = s.name
        feats = self.feats

        if isinstance(s[:1].values[0], (int, float)):  # 时间戳
            ts = self.timestamp2date(s)
        else:
            ts = self.dateStr2date(s)

        ts = ts.progress_map(lambda t: list(self._func(t, feats)))
        return pd.DataFrame(ts.tolist(), columns=feats).add_prefix(add_prefix)

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


if __name__ == '__main__':
    import pandas as pd

    ts = pd.Series([pd.datetime.today()] * 10)
    print(DateTimeFeats().transform(ts))

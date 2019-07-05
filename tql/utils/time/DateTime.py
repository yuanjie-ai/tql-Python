#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : iWork.
# @File         : Time
# @Time         : 2019-06-13 22:17
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 
import time
import numpy as np
import dateutil
import pendulum
from pytz import timezone
"""

from pytz import timezone
cst_tz = timezone('Asia/Shanghai') 
import dateutil
from dateutil.parser import parser 
dateutil.tz.tzstr('Asia/Shanghai') # 时间解析
pd.to_datetime(ts, errors='coerce', infer_datetime_format=True) # pandas调用dateutil的时间解析

"""

class DateTime(object):
    timezoneMap = {"CST": "Asia/Shanghai"}

    def __init__(self):
        self.tz = "Asia/Shanghai"

    def time_to_pdate(self, timestamp):
        return pendulum.from_timestamp(timestamp, self.tz)

    def time_to_date_string(self, timestamp):
        return self.time_to_pdate(timestamp).to_date_string()

    def time_to_datetime_string(self, timestamp):
        return self.time_to_pdate(timestamp).to_datetime_string()

    @property
    def nowTime(self):
        return self.nowDate.timestamp()

    @property
    def nowDate(self):
        return pendulum.now(self.tz)

    @property
    def timezone(self):
        return time.strftime("%Z", time.localtime())  # 获取当前时区


if __name__ == '__main__':
    dt = DateTime()
    print(dt.nowDate)
    print(dt.nowTime)
    print(dt.time_to_date_string(1551843001))
    print(dt.time_to_datetime_string(1551843001))

    from dateutil.relativedelta import relativedelta
    import datetime

    today = datetime.date.today()  # 今天

    yesterday = today - datetime.timedelta(days=1)  # 昨天
    Lastweek = today - datetime.timedelta(days=7)  # 上周
    Nearly_month = today - datetime.timedelta(days=30)  # 前30天
    Last_month = datetime.date.today() - relativedelta(months=1)  # 上月
    Last_year = datetime.date.today() - relativedelta(months=12)  # 去年

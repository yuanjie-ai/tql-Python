#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : iWork.
# @File         : delta
# @Time         : 2019-06-13 22:15
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

# https://www.cnblogs.com/sunshineyang/p/6818834.html
import datetime
from dateutil.relativedelta import relativedelta

d1 = datetime.datetime.today()
d2 = d1 + relativedelta(months=1)

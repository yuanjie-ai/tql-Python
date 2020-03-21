#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : demo
# @Time         : 2019-09-16 15:23
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 
"""
https://www.cnblogs.com/zhaoyingjie/p/9664081.html
"""
import asyncio
from datetime import datetime
import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler

# scheduler = BlockingScheduler()
# scheduler = BackgroundScheduler() # 保持主进程活着
scheduler = AsyncIOScheduler() # asyncio.get_event_loop().run_forever()


@scheduler.scheduled_job('interval', seconds=3)
def tick():
    os.system("echo `date` >> /Users/yuanjie/Desktop/Projects/Python/tql-Python/log.txt")
    print('Tick! The time is: %s' % datetime.now())


scheduler.start()
while 1:
    pass

# asyncio.get_event_loop().run_forever()
# if __name__ == '__main__':
#
#     scheduler.add_job(tick, 'interval', seconds=3)
#     print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
#
#     try:
#         scheduler.start()
#     except (KeyboardInterrupt, SystemExit):
#         pass

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : illegal_char
# @Time         : 2019-09-03 17:36
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 
import re

"""https://www.jianshu.com/p/4958bcdea12a"""


# def illegal_char(s):
#     s = re.compile(r"""^[\u4e00-\u9fa5\u0041-\u005A\u0061-\u007A\u0030-\u0039!@#$%^&*()-=[]{}\\;':",./<>?/*\+]+""") \
#         .sub('', s)
#
#     return s
#
# if __name__ == '__main__':
#     s = "《魔兽世界》官方宣布，为了维护玩家们的游戏体验，" \
#         "将为怀旧服高负载服务器的玩家们提供免费的角色定向转移服务，" \
#         "更多的详情将在晚些时候公布。官方也将在今晚18点新增两个PVP服务器阿什坎迪与怀特迈恩。 ​​​​"
#     print(illegal_char(s))

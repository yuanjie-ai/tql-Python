#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : newsSummary
# @Time         : 2019-08-13 10:19
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

from aip import AipNlp


APP_ID = '15696121'
API_KEY = 'md9ONR0cj5pvF9oxYlg9MIMg'
SECRET_KEY = 'iYGkDYuW4XDGXjMtXPZclUplLhiBNBgQ'

client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
content = """
算法可大致分为基本算法、数据结构的算法、数论算法、计算几何的算法、图的算法、动态规划以及数值分析、加密算法、排序算法、检索算法、随机化算法、并行算法、厄米变形模型、随机森林算法。
算法可以宽泛的分为三类，
一，有限的确定性算法，这类算法在有限的一段时间内终止。他们可能要花很长时间来执行指定的任务，但仍将在一定的时间内终止。这类算法得出的结果常取决于输入值。
二，有限的非确定算法，这类算法在有限的时间内终止。然而，对于一个（或一些）给定的数值，算法的结果并不是唯一的或确定的。
三，无限的算法，是那些由于没有定义终止定义条件，或定义的条件无法由输入的数据满足而不终止运行的算法。通常，无限算法的产生是由于未能确定的定义终止条件。
"""

maxSummaryLen = 160

""" 调用新闻摘要接口 """
client.newsSummary(content, maxSummaryLen)

""" 如果有可选参数 """
options = {}
options["title"] = "标题"

""" 带参数调用新闻摘要接口 """
print(client.newsSummary(content, maxSummaryLen, options))

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : args
# @Time         : 2019-11-01 14:46
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :

# name or flags - 选项字符串的名字或者列表，例如foo 或者-f, --foo。
# action - 在命令行遇到该参数时采取的基本动作类型。
# nargs - 应该读取的命令行参数数目。
# const - 某些action和nargs选项要求的常数值。
# default - 如果命令行中没有出现该参数时的默认值。
# type - 命令行参数应该被转换成的类型。
# choices - 参数可允许的值的一个容器。
# required - 该命令行选项是否可以省略（只针对可选参数）。
# help - 参数的简短描述。
# metavar - 参数在帮助信息中的名字。
# dest - 给parse_args()返回的对象要添加的属性名称。
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbosity", help="increase output verbosity")

args = parser.parse_args()
# print(args.v)
print(args.verbosity) # 以--为主


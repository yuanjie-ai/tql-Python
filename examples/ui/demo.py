#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : demo
# @Time         : 2019-08-09 13:16
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


import PySimpleGUI as sg

# layout = [
#     [sg.Text('Enter a Number')],
#     [sg.Input()],
#     [sg.OK()]
# ]
#
# event, (number,) = sg.Window('Enter a number example').Layout(layout).Read()
#
# sg.Popup(event, number)

layout = [
[sg.Text('你的学历是',auto_size_text=True)],
[sg.Checkbox('游泳',default=True)],   #h 或者 v 表示水平或者垂直
[sg.Checkbox('篮球')],
[sg.Checkbox('足球')],
[sg.Checkbox('羽毛球')],
[sg.OK('确认',auto_size_button=True)]
]

with sg.FlexForm('复选框',auto_size_text=True) as form:
    button_name,choices = form.Layout(layout).Read()
    sg.Popup(button_name,choices)

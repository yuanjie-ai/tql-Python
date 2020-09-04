#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : s
# @Time         : 2019-11-01 10:23
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :

import os
import time
import datetime
import streamlit as st
import numpy as np
import pandas as pd

st.title("Streamlit App")  # st.markdown("# Push Report")
# 刷新
st.button('Re-Run')

st.write("## 输入")
_ = st.time_input('设置时间', datetime.time(8, 45))
st.write('time_input:', _)  # 支持 markdown

_ = st.date_input('设置日期', datetime.datetime.today())
st.write('date_input:', _)

_ = st.number_input('设置数值', 666)
st.write('number_input:', _)

_ = st.text_input('设置文本', 'text_input')
st.write('text_input:', _)

st.write("## 选项")
_ = st.selectbox('下拉项', range(5))
st.write('selectbox:', _)

_ = st.multiselect('多选项', 'abcde', 'abc')
st.write('You selected:', _)

_ = st.checkbox('小框框')
st.write('小框框:', _)


x = st.slider('Select a value')
st.write(x, 'squared is', x * x)

# 拉取 Mongo 数据
dataframe = pd.DataFrame(np.random.randn(3, 5), columns=('col %d' % i for i in range(5)))
st.dataframe(dataframe.style.highlight_max(axis=0))  # st.table

# image
from PIL import Image

image = Image.open('/Users/yuanjie/Desktop/xm.jpg')
st.write("## 图片")
st.image(image, caption='Sunrise by the mountains', use_column_width=False)

# info
st.success('This is a success message!')



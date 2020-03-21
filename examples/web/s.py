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
import streamlit as st

x = st.slider('Select a value')
st.write(x, '# squared is', x * x)

import time
import numpy as np

progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()
last_rows = np.random.randn(1, 1)
chart = st.line_chart(last_rows)

for i in range(1, 10):
    new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
    status_text.text("%i%% Complete" % i)
    chart.add_rows(new_rows)
    progress_bar.progress(i)
    last_rows = new_rows

progress_bar.empty()

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.

# @st.cache()()
st.button("Re-run")

import numpy as np
import pandas as pd
from pandas_profiling import ProfileReport
# 结合redis
dataframe = pd.DataFrame(
    np.random.randn(3, 5),
    columns=('col %d' % i for i in range(5)))

profile = ProfileReport(dataframe)

st.markdown("# a")

st.write(profile.to_html(), unsafe_allow_html=True)
st.write(dataframe, unsafe_allow_html=True)



st.dataframe(dataframe.style.highlight_max(axis=0))


# if __name__ == '__main__':
# import os
# os.system("streamlit run s.py")

# os.system("streamlit run s.py")

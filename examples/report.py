#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : report
# @Time         : 2019-07-10 13:38
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


import numpy as np
import pandas as pd
import pandas_profiling

# df = pd.DataFrame(
#     np.random.rand(100, 5),
#     columns=['a', 'b', 'c', 'd', 'e']
# )

def get_html_str(**kwargs):
    df_dic = kwargs['df_dic']
    df = pd.DataFrame(df_dic)
    return df.profile_report().to_html()


from restful_api import Api
api = Api('/post1', get_html_str, verbose=False)
api.app.run('0.0.0.0')


# import numpy as np
# import pandas_utils as pd
# import pandas_profiling
#
# df = pd.DataFrame(
#     np.random.rand(100, 5),
#     columns=['a', 'b', 'c', 'd', 'e']
# )
#
# import requests
#
# url = 'http://0.0.0.0:8000/post1'
# json = {'df_dic': df.to_dict()}
# r = requests.post(url, json=json)
# html_str = r.json()['Score']
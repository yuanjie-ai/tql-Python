#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : restful
# @Time         : 2019-07-02 10:48
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

import flask
import pandas as pd

import tensorflow as tf

# 实例化 flask
app = flask.Flask(__name__)


# 我们需要重新定义我们的度量函数，
# 从而在加载模型时使用它


def auc(y_true, y_pred):
    # auc = tf.metrics.auc(y_true, y_pred)[1]
    # keras.backend.get_session().run(tf.local_variables_initializer())
    return auc



# 将预测函数定义为一个端点
@app.route("/predict", methods=["GET","POST"])
def predict():
    data = {"success": False}

    params = flask.request.json
    if (params == None):
        params = flask.request.args

    # 若发现参数，则返回预测值
    if (params != None):
        x=pd.DataFrame.from_dict(params, orient='index').transpose()
        # with graph.as_default():
        #     # data["prediction"] = str(model.predict(x)[0][0])
        #     data["success"] = True

    # 返回Jason格式的响应
    return flask.jsonify(data)

# 启动Flask应用程序，允许远程连接
if __name__ == "__main__":
    app.run(host='0.0.0.0')

#!/usr/bin/env bash
# @Project      : tql-Python
# @Time         : 2019-08-15 18:07
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : ${DESCRIPTION}

# rest
modelpath="/Users/yuanjie/Desktop/Projects/Python/tql-Python/examples/deploy/mlruns/0/3f52da7ab25649de825ed8d344ea4be6/artifacts/model"
mlflow models serve -m $modelpath --port 7777 --no-conda

# post
curl -d '{"columns":[0],"index":[0,1],"data":[[1],[-1]]}' -H 'Content-Type: application/json'  localhost:5000/invocations


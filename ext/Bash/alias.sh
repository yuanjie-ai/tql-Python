#!/usr/bin/env bash
# https://blog.csdn.net/foolsong/article/details/77940379

SCALA_HOME=/usr/local/Cellar/scala-2.12.4
SPARK_HOME=/usr/local/Cellar/spark-2.2.0-bin-hadoop2.7
PYTHON_HOME=/Users/yuanjie/Desktop/intelpython3
REDIS_HOME=/usr/local/Cellar/redis/5.0.3

export PATH=$REDIS_HOME/bin:$PYTHON_HOME/bin:$PATH

# alias
alias py='python'
alias jn='jupyter-notebook'
alias jlab='jupyterlab'
alias http='cd /Users/yuanjie/Desktop/Data && python -m http.server 8080'

eval $(thefuck --alias)
alias c='clear'
alias bi='brew install'
alias bci='brew cask install'
alias ep='vim .zshrc'
alias sp='source .zshrc'
alias ll='ls -l'


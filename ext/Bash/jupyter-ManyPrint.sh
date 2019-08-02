#!/usr/bin/env bash
# @Project      : tql-Python
# @Time         : 2019-07-19 18:33
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : ${DESCRIPTION}

echo 'c = get_config()
# Run all nodes interactively
c.InteractiveShell.ast_node_interactivity = "all"
c.NotebookApp.contents_manager_class="jupytext.TextFileContentsManager"' >> .ipython/profile_default/ipython_config.py
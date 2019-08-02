#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'matplotlib_chinese'
__author__ = 'JieYuan'
__mtime__ = '19-4-1'
"""
import os
import matplotlib
import matplotlib.pyplot as plt
from pathlib import Path

from matplotlib.font_manager import _rebuild


def chinese_setting(url="http://cnbj1.fds.api.xiaomi.com/browser-algo-nanjing/data/SimHei.ttf"):
    """
    :param url: SimHei字体下载链接
    :return:
    """
    print('开始设置中文...')
    matplotlibrc_path = Path(matplotlib.matplotlib_fname())
    ttf_path = matplotlibrc_path.parent.__str__() + '/fonts/ttf'
    ttf_url = 'https://raw.githubusercontent.com/Jie-Yuan/Jie-Yuan.github.io/master/SimHei.ttf' if url is None else url
    if list(Path(ttf_path).glob('SimHei.ttf')):
        pass
    else:
        print('下载字体...')
        os.popen("cd %s && wget %s" % (ttf_path, ttf_url)).read()
        os.popen("rm -rf ~/.matplotlib/*.cache").read()

    print('设置字体...')
    setting1 = 'font.family: sans-serif'
    setting2 = 'font.sans-serif: SimHei, Bitstream Vera Sans, Lucida Grande, Verdana, Geneva, Lucid, Arial, Helvetica, Avant Garde, sans-serif'
    setting3 = 'axes.unicode_minus: False'
    os.system('echo > %s' % matplotlibrc_path)
    os.system('echo %s >> %s' % (setting1, matplotlibrc_path))
    os.system('echo %s >> %s' % (setting2, matplotlibrc_path))
    os.system('echo %s >> %s' % (setting3, matplotlibrc_path))

    _rebuild()
    print('请重启kernel测试...')


if __name__ == '__main__':
    chinese_setting()
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], label='中文测试')
    ax.legend()
    plt.show()

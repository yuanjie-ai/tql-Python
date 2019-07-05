# coding: utf-8

def startswith(ls, pattern):
    """
    :param ls: 字符串列表
    :param pattern: 正则表达式
    :return: 匹配到的规定开头字符串列表
    """
    return [i for i in ls if re.match(pattern, i)]

get_num = lambda x: ''.join(filter(str.isdigit, x)) # 从字符串中提取数字
 

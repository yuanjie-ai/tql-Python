# coding: utf-8
__title__ = 'data_transform'
__author__ = 'JieYuan'
__mtime__ = '2018/2/13'


# 聚合函数
class Agg(object):
    @staticmethod
    def mode(x):
        """
        因mode需至少重复2次才可用，故需判断异常
        """
        try:
            _mode = x.mode()[0]
        except:
            return x.values[0]
        else:
            return _mode

    @staticmethod
    def count_zero(x):
        return len(x) - np.sum(x)

    @staticmethod
    def count_null(x):
        return x.isnull().sum()

    @staticmethod
    def gr_agg(df, by_name, col_name, *functions):
        """
        positional argument follows keyword argument相对位置指代参数
        """
        gr = df.groupby(by_name)
        mapper = lambda x: col_name + '_' + x if x != by_name else by_name  # col_name_sum
        return gr[col_name].agg(functions).reset_index().rename(columns=mapper)

    @staticmethod
    def nlargest(df, by_name, col_name, n=1):
        """
        col_name top K
        """
        return df.sort_values(col_name).groupby(by_name).tail(n)

    @staticmethod
    def nsmallest(df, by_name, col_name, n=1):
        return df.sort_values(col_name).groupby(by_name).head(n)

    @classmethod
    def nmost(cls, df, by_name, col_name, n=3):
        """
        col_name 最多的前几个 pandas新加列名
        """
        df = df.groupby([by_name, col_name], as_index=False)[col_name].agg({'_count': 'count'})
        return df.pipe(cls.nlargest, by_name, '_count', n).drop('_count', 1).rename(
            columns={col_name: col_name + '_nmost'})

    @classmethod
    def nleast(cls, df, by_name, col_name, n=3):
        df = df.groupby([by_name, col_name], as_index=False)[col_name].agg({'_count': 'count'})
        return df.pipe(cls.nsmallest, by_name, '_count', n).drop('_count', 1).rename(
            columns={col_name: col_name + '_nleast'})


# 数据变形
class Reshape(object):
    def __init__(self):
        pass

    @staticmethod
    def explode(df, col, pat=None, drop_col=True):
        """
        :param df:
        :param col: col name
        :param pat: String or regular expression to split on. If None, splits on whitespace
        :param drop_col: drop col is Yes or No
        :return: hive explode
        """
        data = df.copy()
        data_temp = data[col].str.split(pat=pat, expand=True).stack().reset_index(level=1, drop=True).rename(
            col + '_explode')
        if drop_col:
            data.drop(col, 1, inplace=True)
        return data.join(data_temp)

    # df.a.str.split('|', expand=True) 'a|b|c' -> 'a', 'b', 'c'

    @staticmethod
    def crossJoin(df1, df2):
        __addCol = lambda x: x.assign(__col=1)
        return __addCol(df1).merge(__addCol(df2), on='__col').drop('__col', 1)


# lag/lead
def lag(df, by_name, col_name, n=1):
    df = df.copy()
    df[col_name + '_' + str(n)] = df.groupby(by_name)[col_name].shift(n)
    return df

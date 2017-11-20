class DF2FFM(object):
    @classmethod
    def df2ffm(cls, df, col_list):
        field_dict = cls.__tran_field_dict(col_list)
        ffm_data = pd.DataFrame()
        for col in col_list:
            tran_data, _ = cls.__tran_ffm_data(df, col, field_dict)
            ffm_data = pd.concat([ffm_data, tran_data], axis=1)
        return ffm_data

    @staticmethod
    def __tran_field_dict(col_list):  ## field数值转换
        return dict(zip(col_list, range(len(col_list))))

    @staticmethod
    def __tran_ffm_data(df, col, field_dict):  ## index数值替换
        # global field_dict
        index_dict = dict(zip(df[col].unique(), range(len(df[col].unique()))))
        trans = df[col].apply(lambda x: (field_dict[col], index_dict[x], 1))
        return trans, index_dict

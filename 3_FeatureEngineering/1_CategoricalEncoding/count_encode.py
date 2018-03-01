def count_encode(df: pd.Series):
    from collections import Counter
    return df.replace(Counter(df))

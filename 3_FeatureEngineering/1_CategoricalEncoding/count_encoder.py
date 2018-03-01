def count_encoder(df: pd.Series):
    from collections import Counter
    return df.replace(Counter(df))

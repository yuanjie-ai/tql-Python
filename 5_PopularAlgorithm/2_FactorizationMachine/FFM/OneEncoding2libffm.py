def df2libffm(df, field_Category, field_Numeric=[]):
    libffm = []
    num_n = len(field_Numeric)
    csr = OneHotEncoder().fit_transform(df[field_Category])
    for i in range(len(csr.indptr) - 1):
        ls = []
        k = csr.indptr[i + 1] - csr.indptr[i]
        for j in range(k):
            ls.append((k - j + num_n, csr.indices[i * k + j] + num_n, 1))
        libffm.append(ls)
        
    if field_Numeric:
        for i in range(len(libffm)):
            for j in range(len(field_Numeric)):
                libffm[i].append((j + 1, j + 1, df[field_Numeric[j]].iloc[i]))
    return libffm

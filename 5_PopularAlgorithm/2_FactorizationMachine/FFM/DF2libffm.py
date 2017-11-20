import hashlib
import pandas as pd

class DF2libffm(object):
    def __init__(self, field_names):
        self.field_names = field_names
        
    def df2libffm(self, df):
        df_temp = pd.DataFrame()
        for row in df.values:
            features = []
            for field, feature in enumerate(self._gen_features(row)):
                features.append((field, self._hashstr(feature, 1e+6), 1))
            df_temp = pd.concat([df_temp, pd.DataFrame([features])])
        return df_temp
    
    def _gen_features(self, row):
        features = []
        for i, field in enumerate(self.field_names):
            value = row[i]
            key = field + '-' + str(value)
            features.append(key)
        return features
    
    def _hashstr(self, string, nr_bins=1e+6):
        return int(hashlib.md5(string.encode('utf8')).hexdigest(), 16) % (int(nr_bins) - 1) + 1

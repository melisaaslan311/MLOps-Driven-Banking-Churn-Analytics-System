import pandas as pd
from sklearn.preprocessing import OneHotEncoder

def transform(df: pd.DataFrame) -> pd.DataFrame:
    df= df.drop_duplicates()
    ohe = OneHotEncoder(sparse_output=False).set_output(transform="pandas")
    encoded_data = ohe.fit_transform(df[['country', 'gender']])
    df = pd.concat([df, encoded_data], axis=1).drop(['country', 'gender'], axis=1)
    return df


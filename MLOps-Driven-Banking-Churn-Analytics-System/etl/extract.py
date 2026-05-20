import pandas as pd
from config.settings import RAW_PATH

def extract() -> pd.DataFrame:
    df=pd.read_csv(RAW_PATH)
    print("raw data loaded:",df.shape)
    return df

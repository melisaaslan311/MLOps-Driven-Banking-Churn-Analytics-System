import pandas as pd
from sqlalchemy import create_engine
from config.settings import MYSQL_URI

def load(df):
    engine = create_engine(MYSQL_URI)
    df.to_sql("customers", engine, if_exists="replace", index=False)
    print("Loaded to MySQL!")

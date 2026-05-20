import logging
from etl.load import load
from etl.extract import extract
from etl.transform import transform

from config.settings import LOG_PATH, PROCESSED_PATH
#Gerçek projelerde kodun başında durup ekranı izlemezsin. 
#Bir hata olduğunda LOG_PATH içindeki dosyayı açıp "Saat kaçta, hangi aşamada hata olmuş?" diye bakarsın.

logging.basicConfig(filename=LOG_PATH,
                    level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

def run_pipeline():
    logging.info("Pipline Started")
    
    df= extract()
    logging.info(f"Extracted {len(df)} rows")
    
    df= transform(df)
    logging.info("Transform Comleted")
    
    df.to_csv(PROCESSED_PATH,index=False)
    logging.info("Saved CSV")
    
    load(df)
    logging.info("Loaded MySQL")
    
    logging.info("Pipline finished")


if __name__ == "__main__":
    run_pipeline()

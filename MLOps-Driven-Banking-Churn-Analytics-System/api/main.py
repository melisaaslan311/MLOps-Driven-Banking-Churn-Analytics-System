import os
import joblib
import pandas as pd
from fastapi import FastAPI

app = FastAPI()
current_dir = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(current_dir, "models", "xgboost_model.pkl")
scaler_path = os.path.join(current_dir, "models", "scaler.pkl")

try:
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    print("✅ Model ve Scaler başarıyla yüklendi.")
except FileNotFoundError:
    print(f"❌ HATA: Dosya bulunamadı! Aranan yol: {model_path}")
    
@app.post("/predict")
def predict(data: dict):
    try:
        df = pd.DataFrame([data])
        
        # Hata ayıklama için: Modelin beklediği sütunlarla gelenleri kıyasla
        print(f"Gelen Sütunlar: {df.columns.tolist()}")
        
        df_scaled = scaler.transform(df)
        prob = model.predict_proba(df_scaled)[0][1]
        
        return {"churn_probability": float(prob), "status": "Riskli" if prob > 0.5 else "Güvenli"}
    
    except Exception as e:
        print(f"❌ TAHMİN HATASI: {str(e)}")
        return {"error": str(e)}

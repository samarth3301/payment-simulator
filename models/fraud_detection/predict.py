import joblib
import pandas as pd
from .preprocess import preprocess_data

def predict_new(csv_path: str, model_path: str):
    model = joblib.load(model_path)
    X, y, df = preprocess_data(csv_path)
    df['Prediction'] = model.predict(X)
    df['Prediction'] = df['Prediction'].map({0: "NOT_SUSPICIOUS", 1: "SUSPICIOUS"})
    return df[['Transaction ID','Amount','Sender UPI ID','Receiver UPI ID','Prediction']]

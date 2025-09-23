from models.fraud_detection.predict import predict_new
import pandas as pd

if __name__ == "__main__":
    results = predict_new("data/transactions.csv", "model/fraud_model.joblib")
    print(results.head(20))

from models.fraud_detection.train import train_model

if __name__ == "__main__":
    train_model("data/transactions.csv", "model/fraud_model.joblib")

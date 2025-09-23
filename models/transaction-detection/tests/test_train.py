from models.fraud_detection.train import train_model
import os

def test_train():
    model_path = "models/test_model.joblib"
    train_model("data/transactions.csv", model_path)
    assert os.path.exists(model_path)

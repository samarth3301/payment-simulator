from models.fraud_detection.preprocess import preprocess_data

def test_preprocess():
    X, y, df = preprocess_data("data/transactions.csv")
    assert not X.empty
    assert len(X) == len(y)

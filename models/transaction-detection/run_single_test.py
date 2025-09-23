import pandas as pd
from models.fraud_detection.utils import load_model
import datetime

def prepare_single_transaction(sender_upi, receiver_upi, amount, state, city, timestamp):

    hour = pd.to_datetime(timestamp, format="%d-%m-%Y %H:%M").hour

    # NOTE: For unseen UPI IDs / states, we’ll just hash them into integers
    sender_code = abs(hash(sender_upi)) % 10000
    receiver_code = abs(hash(receiver_upi)) % 10000
    state_code = abs(hash(state)) % 1000
    city_code = abs(hash(city)) % 1000

    return pd.DataFrame([{
        "Amount": amount,
        "Hour": hour,
        "SenderUPI": sender_code,
        "ReceiverUPI": receiver_code,
        "StateCode": state_code,
        "CityCode": city_code
    }])

if __name__ == "__main__":
    model = load_model("model/fraud_model.joblib")

    # 🧪 Some random unseen transactions
    test_transactions = [
        {
            "sender": "randomguy@upi",
            "receiver": "unknown@upi",
            "amount": 99999,
            "state": "Delhi",
            "city": "New Delhi",
            "timestamp": "01-09-2025 02:45"  # odd hour
        },
        {
            "sender": "ayush@upi",
            "receiver": "friend@upi",
            "amount": 250,
            "state": "West Bengal",
            "city": "Kolkata",
            "timestamp": "01-09-2025 14:30"  # normal afternoon
        },
        {
            "sender": "scammer@upi",
            "receiver": "muleaccount@upi",
            "amount": 65000,
            "state": "Maharashtra",
            "city": "Mumbai",
            "timestamp": "01-09-2025 23:59"  # suspicious time + high amount
        },
    ]

    for t in test_transactions:
        df = prepare_single_transaction(
            t["sender"], t["receiver"], t["amount"],
            t["state"], t["city"], t["timestamp"]
        )
        pred = model.predict(df)[0]
        label = "SUSPICIOUS" if pred == 1 else "NOT_SUSPICIOUS"
        print(f"Transaction {t['sender']} -> {t['receiver']} | Amount: {t['amount']} | Prediction: {label}")

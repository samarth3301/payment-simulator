import pandas as pd
import os
from models.fraud_detection.predict import predict_new
from models.fraud_detection.utils import load_model

class FraudDetectionService:
    def __init__(self, model_path="model/fraud_model.joblib"):
        self.model_path = model_path
        self.model = None

    def load_model(self):
        """Load the fraud detection model if not already loaded."""
        if self.model is None and os.path.exists(self.model_path):
            self.model = load_model(self.model_path)
        return self.model is not None

    def check_transaction_fraud(self, transaction):
        """
        Check if a transaction is fraudulent.

        Args:
            transaction: Transaction model instance

        Returns:
            dict: {'is_suspicious': bool, 'score': float or None}
        """
        if not self.load_model():
            # If model not available, assume not suspicious
            return {'is_suspicious': False, 'score': None}

        try:
            # Create a DataFrame with transaction data matching training format
            # Include all columns that the model expects
            transaction_data = {
                'Transaction ID': [transaction.id],
                'Amount': [float(transaction.amount)],
                'Sender UPI ID': [transaction.sender_upi_id],
                'Receiver UPI ID': [transaction.receiver_upi_id],
                'Timestamp': [transaction.timestamp.strftime('%d-%m-%Y %H:%M')],  # Format as expected
                'State': ['Unknown'],  # Default value since we don't have this data
                'City': ['Unknown'],   # Default value since we don't have this data
            }

            df = pd.DataFrame(transaction_data)

            # Save to temporary CSV for prediction
            temp_csv = f"/tmp/transaction_{transaction.id}.csv"
            df.to_csv(temp_csv, index=False)

            # Make prediction
            result_df = predict_new(temp_csv, self.model_path)

            # Clean up temp file
            if os.path.exists(temp_csv):
                os.remove(temp_csv)

            if not result_df.empty:
                prediction = result_df.iloc[0]['Prediction']
                is_suspicious = prediction == "SUSPICIOUS"
                # For now, we'll use a binary score (0 or 1)
                score = 1.0 if is_suspicious else 0.0
                return {'is_suspicious': is_suspicious, 'score': score}

        except Exception as e:
            print(f"Fraud detection error: {e}")
            # On error, assume not suspicious
            return {'is_suspicious': False, 'score': None}

        return {'is_suspicious': False, 'score': None}

# Global instance
fraud_service = FraudDetectionService()
from app.config.database import db
from datetime import datetime
from enum import Enum

class TransactionStatus(Enum):
    PENDING = "pending"
    FAILED = "failed"
    SUCCESS = "success"

class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.String(50), primary_key=True)  # Transaction ID
    amount = db.Column(db.Numeric(10, 2), nullable=False)  # Amount in rupees (supports up to 1 lakh)
    sender_upi_id = db.Column(db.String(100), nullable=False)
    receiver_upi_id = db.Column(db.String(100), nullable=False)  # Related to mule accounts
    sender_name = db.Column(db.String(100), nullable=False)
    receiver_name = db.Column(db.String(100), nullable=False)
    sender_phone = db.Column(db.String(15), nullable=False)  # Phone number
    receiver_phone = db.Column(db.String(15), nullable=False)  # Phone number
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)  # Most important - indexed
    
    # New fields for payment simulation
    status = db.Column(db.String(20), nullable=False, default=TransactionStatus.PENDING.value)
    fraud_flag = db.Column(db.Boolean, default=False)
    fraud_score = db.Column(db.Float, nullable=True)

    # Constraints
    __table_args__ = (
        db.CheckConstraint('amount > 0 AND amount <= 100000', name='amount_range'),  # 1 to 1 lakh
        db.CheckConstraint("status IN ('pending', 'failed', 'success')", name='status_check'),
    )

    def __repr__(self):
        return f'<Transaction {self.id}: ₹{self.amount} from {self.sender_upi_id} to {self.receiver_upi_id}>'

    def to_dict(self):
        """Convert transaction to dictionary for API responses."""
        return {
            'id': self.id,
            'amount': float(self.amount),
            'sender_upi_id': self.sender_upi_id,
            'receiver_upi_id': self.receiver_upi_id,
            'sender_name': self.sender_name,
            'receiver_name': self.receiver_name,
            'sender_phone': self.sender_phone,
            'receiver_phone': self.receiver_phone,
            'timestamp': self.timestamp.isoformat(),
            'status': self.status,
            'fraud_flag': self.fraud_flag,
            'fraud_score': self.fraud_score
        }
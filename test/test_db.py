from app import create_app
from app.models.transactions import Transaction
from app.config.database import db
import uuid
from datetime import datetime

def test_database():
    app = create_app()

    with app.app_context():
        print("🔄 Testing PostgreSQL database connection...")

        # Create tables if they don't exist
        db.create_all()
        print("✅ Tables created/verified")

        # Test creating a transaction
        transaction_id = str(uuid.uuid4())[:16].upper()
        transaction = Transaction(
            id=transaction_id,
            amount=50000.75,
            sender_upi_id='test_sender@upi',
            receiver_upi_id='test_mule@upi',
            sender_name='Test Sender',
            receiver_name='Test Mule Account',
            sender_phone='+919876543210',
            receiver_phone='+919876543211',
            timestamp=datetime.utcnow()
        )

        db.session.add(transaction)
        db.session.commit()
        print("✅ Transaction created successfully")

        # Test querying
        transactions = Transaction.query.all()
        print(f"✅ Found {len(transactions)} transaction(s)")

        for t in transactions:
            print(f"""
📄 Transaction Details:
   ID: {t.id}
   Amount: ₹{t.amount}
   Sender: {t.sender_name} ({t.sender_upi_id})
   Receiver: {t.receiver_name} ({t.receiver_upi_id})
   Sender Phone: {t.sender_phone}
   Receiver Phone: {t.receiver_phone}
   Timestamp: {t.timestamp}
            """)

        print("🎉 PostgreSQL database test completed successfully!")

if __name__ == "__main__":
    test_database()

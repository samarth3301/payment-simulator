from flask import Blueprint, request, jsonify
from app.config.database import db
from app.models.transactions import Transaction
import uuid
from datetime import datetime
import random

transaction_bp = Blueprint('transaction', __name__)

@transaction_bp.route("/", methods=['GET'])
def get_transactions():
    """Get all transactions."""
    transactions = Transaction.query.order_by(Transaction.timestamp.desc()).all()
    return jsonify([t.to_dict() for t in transactions])

@transaction_bp.route("/", methods=['POST'])
def create_transaction():
    """Create a new transaction."""
    data = request.get_json()

    required_fields = [
        'amount', 'sender_upi_id', 'receiver_upi_id',
        'sender_name', 'receiver_name', 'sender_phone', 'receiver_phone'
    ]

    # Validate required fields
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400

    # Validate amount range
    try:
        amount = float(data['amount'])
        if amount <= 0 or amount > 100000:
            return jsonify({'error': 'Amount must be between 1 and 100,000 rupees'}), 400
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid amount format'}), 400

    # Generate unique transaction ID
    transaction_id = str(uuid.uuid4())[:16].upper()

    transaction = Transaction(
        id=transaction_id,  # type: ignore
        amount=amount, # type: ignore
        sender_upi_id=data['sender_upi_id'], # type: ignore
        receiver_upi_id=data['receiver_upi_id'], # type: ignore
        sender_name=data['sender_name'], # type: ignore
        receiver_name=data['receiver_name'], # type: ignore
        sender_phone=data['sender_phone'], # type: ignore
        receiver_phone=data['receiver_phone'], # type: ignore
        timestamp=datetime.now() # type: ignore
    )

    try:
        db.session.add(transaction)
        db.session.commit()
        return jsonify(transaction.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create transaction', 'details': str(e)}), 500

@transaction_bp.route("/<transaction_id>", methods=['GET'])
def get_transaction(transaction_id):
    """Get a specific transaction by ID."""
    transaction = Transaction.query.get_or_404(transaction_id)
    return jsonify(transaction.to_dict())

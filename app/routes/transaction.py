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

@transaction_bp.route("/<transaction_id>/status", methods=['PUT'])
def update_transaction_status(transaction_id):
    """Update transaction status (pending -> failed/success)."""
    transaction = Transaction.query.get_or_404(transaction_id)

    data = request.get_json()
    if not data or 'status' not in data:
        return jsonify({'error': 'status is required'}), 400

    new_status = data['status'].lower()
    if new_status not in ['pending', 'failed', 'success']:
        return jsonify({'error': 'Invalid status. Must be pending, failed, or success'}), 400

    # Business logic: can only change from pending
    if transaction.status != 'pending':
        return jsonify({'error': f'Cannot change status from {transaction.status}'}), 400

    # If trying to set to success, check fraud first
    if new_status == 'success':
        from app.services.fraud_service import fraud_service
        fraud_result = fraud_service.check_transaction_fraud(transaction)

        transaction.fraud_flag = fraud_result['is_suspicious']
        transaction.fraud_score = fraud_result['score']

        # If suspicious, don't allow success but save the fraud detection results
        if fraud_result['is_suspicious']:
            try:
                db.session.commit()
                return jsonify({
                    'error': 'Transaction flagged as suspicious',
                    'fraud_score': fraud_result['score'],
                    'message': 'Cannot complete suspicious transaction'
                }), 400
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': 'Failed to update fraud detection results', 'details': str(e)}), 500

    transaction.status = new_status

    try:
        db.session.commit()
        return jsonify({
            'message': f'Transaction status updated to {new_status}',
            'transaction': transaction.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update status', 'details': str(e)}), 500

@transaction_bp.route("/<transaction_id>/process", methods=['POST'])
def process_transaction(transaction_id):
    """Process a pending transaction (simulate payment processing)."""
    transaction = Transaction.query.get_or_404(transaction_id)

    if transaction.status != 'pending':
        return jsonify({'error': f'Transaction is already {transaction.status}'}), 400

    # Simulate processing delay and random success/failure
    import random
    success_rate = 0.8  # 80% success rate

    if random.random() < success_rate:
        # Attempt to set as success (will check fraud)
        update_data = {'status': 'success'}
    else:
        update_data = {'status': 'failed'}

    # Use the same logic as update status
    from app.services.fraud_service import fraud_service

    if update_data['status'] == 'success':
        fraud_result = fraud_service.check_transaction_fraud(transaction)
        transaction.fraud_flag = fraud_result['is_suspicious']
        transaction.fraud_score = fraud_result['score']

        if fraud_result['is_suspicious']:
            transaction.status = 'failed'  # Mark as failed due to fraud
            db.session.commit()
            return jsonify({
                'message': 'Transaction failed due to fraud detection',
                'fraud_score': fraud_result['score'],
                'transaction': transaction.to_dict()
            }), 200

    transaction.status = update_data['status']

    try:
        db.session.commit()
        return jsonify({
            'message': f'Transaction processed: {transaction.status}',
            'transaction': transaction.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to process transaction', 'details': str(e)}), 500

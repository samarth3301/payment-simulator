# 💳 Payment Simulator API

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0+-black.svg)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-blue.svg)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A comprehensive **payment simulation API** built with Flask and PostgreSQL, featuring **real-time fraud detection** using machine learning. Perfect for testing payment flows, simulating UPI transactions, and evaluating fraud detection algorithms.

## ✨ Features

- 🚀 **RESTful API** - Complete CRUD operations for payment transactions
- 🔍 **AI-Powered Fraud Detection** - Machine learning model trained on transaction patterns
- 📊 **Real-time Processing** - Simulate payment processing with configurable success rates
- 🗄️ **PostgreSQL Database** - Robust data persistence with migrations
- 🐳 **Docker Ready** - Production-ready containerization with Gunicorn
- 📈 **Transaction Analytics** - Status tracking (pending/failed/success)
- 🔒 **Input Validation** - Comprehensive data validation and error handling
- 📱 **UPI Simulation** - Realistic UPI-based payment flows

## 📁 Project Structure

```
payment-simulator/
├── app/
│   ├── __init__.py              # Flask application factory
│   ├── config/
│   │   ├── database.py          # Database configuration
│   │   └── envVars.py           # Environment variables
│   ├── models/
│   │   └── transactions.py      # Transaction data model
│   ├── routes/
│   │   ├── __init__.py
│   │   └── transaction.py       # API endpoints
│   ├── services/
│   │   └── fraud_service.py     # Fraud detection service
│   └── errors/
│       └── handlers.py          # Error handling
├── models/                      # ML models and training scripts
│   ├── fraud_detection/
│   │   ├── predict.py           # Prediction utilities
│   │   ├── preprocess.py        # Data preprocessing
│   │   ├── train.py            # Model training
│   │   └── utils.py            # Helper functions
│   └── transaction-detection/
│       └── run_training.py     # Training script runner
├── data/
│   └── transactions.csv         # Training dataset
├── migrations/                  # Database migrations
├── test/
│   └── test_db.py              # Database tests
├── Dockerfile                   # Production container
├── docker-compose.yml          # Multi-service setup
├── pyproject.toml              # Dependencies & config
├── run.py                      # Application entry point
└── README.md
```

## � Quick Start (Docker)

### Prerequisites
- Docker & Docker Compose
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/samarth3301/payment-simulator.git
   cd payment-simulator
   ```

2. **Start all services**
   ```bash
   docker-compose up -d
   ```

3. **Verify deployment**
   ```bash
   curl http://localhost:8080/
   ```

### Docker Commands

```bash
# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild and restart
docker-compose up --build -d

# Access database
docker-compose exec postgres psql -U webond -d webond

# Run tests
docker-compose exec app python test/test_db.py
```

## 🛠️ Manual Setup (Development)

### Prerequisites
- Python 3.12+
- PostgreSQL 14+
- uv package manager

### Installation

1. **Clone and setup**
   ```bash
   git clone https://github.com/samarth3301/payment-simulator.git
   cd payment-simulator
   ```

2. **Install dependencies**
   ```bash
   uv pip install -e .
   ```

3. **Setup PostgreSQL database**
   ```sql
   CREATE DATABASE webond;
   CREATE USER webond WITH PASSWORD 'weBond@2025!';
   GRANT ALL PRIVILEGES ON DATABASE webond TO webond;
   ```

4. **Configure environment**
   ```bash
   cp .example.env .env
   # Edit .env with your database credentials
   ```

5. **Initialize database**
   ```bash
   uv run flask --app run db init
   uv run flask --app run db migrate -m "Initial migration"
   uv run flask --app run db upgrade
   ```

6. **Start development server**
   ```bash
   uv run python run.py
   ```

## 📡 API Documentation

### Base URL
```
http://localhost:8080
```

### Authentication
No authentication required for this simulation API.

### Endpoints

#### 1. List All Transactions
**GET /**

Returns all transactions ordered by timestamp (newest first).

**Response:**
```json
[
  {
    "id": "TXN1234567890ABCD",
    "amount": 25000.50,
    "sender_upi_id": "john@upi",
    "receiver_upi_id": "mule@upi",
    "sender_name": "John Doe",
    "receiver_name": "Mule Account",
    "sender_phone": "+919876543210",
    "receiver_phone": "+919876543211",
    "timestamp": "2025-09-24T19:30:00",
    "status": "pending",
    "fraud_flag": false,
    "fraud_score": null
  }
]
```

#### 2. Create Transaction
**POST /**

Create a new payment transaction.

**Request Body:**
```json
{
  "amount": 25000.50,
  "sender_upi_id": "john@upi",
  "receiver_upi_id": "mule@upi",
  "sender_name": "John Doe",
  "receiver_name": "Mule Account",
  "sender_phone": "+919876543210",
  "receiver_phone": "+919876543211"
}
```

**Response (201):**
```json
{
  "id": "TXN1234567890ABCD",
  "amount": 25000.50,
  "sender_upi_id": "john@upi",
  "receiver_upi_id": "mule@upi",
  "sender_name": "John Doe",
  "receiver_name": "Mule Account",
  "sender_phone": "+919876543210",
  "receiver_phone": "+919876543211",
  "timestamp": "2025-09-24T19:30:00",
  "status": "pending",
  "fraud_flag": false,
  "fraud_score": null
}
```

**Validation Rules:**
- Amount: 1 - 100,000 INR
- All fields required
- UPI IDs must be valid format

#### 3. Get Transaction Details
**GET /<transaction_id>**

Retrieve details for a specific transaction.

**Response (200):**
```json
{
  "id": "TXN1234567890ABCD",
  "amount": 25000.50,
  "sender_upi_id": "john@upi",
  "receiver_upi_id": "mule@upi",
  "sender_name": "John Doe",
  "receiver_name": "Mule Account",
  "sender_phone": "+919876543210",
  "receiver_phone": "+919876543211",
  "timestamp": "2025-09-24T19:30:00",
  "status": "success",
  "fraud_flag": false,
  "fraud_score": 0.12
}
```

#### 4. Update Transaction Status
**PUT /<transaction_id>/status**

Update transaction status with fraud detection.

**Request Body:**
```json
{
  "status": "success"
}
```

**Response (200):**
```json
{
  "message": "Transaction status updated to success",
  "transaction": {
    "id": "TXN1234567890ABCD",
    "status": "success",
    "fraud_flag": false,
    "fraud_score": 0.12
  }
}
```

**Business Rules:**
- Can only change status from "pending"
- Valid statuses: `pending`, `failed`, `success`
- Success attempts trigger fraud detection
- Suspicious transactions are blocked

#### 5. Process Transaction
**POST /<transaction_id>/process**

Simulate payment processing with random outcomes and fraud detection.

**Response (200):**
```json
{
  "message": "Transaction processed: success",
  "transaction": {
    "id": "TXN1234567890ABCD",
    "status": "success",
    "fraud_flag": false,
    "fraud_score": 0.23
  }
}
```

**Processing Logic:**
- 80% success rate simulation
- Automatic fraud detection on success attempts
- Suspicious transactions marked as failed

## 🗄️ Database Schema

### Transactions Table

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `id` | VARCHAR(50) | Unique transaction ID | Primary Key |
| `amount` | NUMERIC(10,2) | Transaction amount in INR | 1 ≤ amount ≤ 100,000 |
| `sender_upi_id` | VARCHAR(100) | Sender's UPI ID | Not Null |
| `receiver_upi_id` | VARCHAR(100) | Receiver's UPI ID | Not Null |
| `sender_name` | VARCHAR(100) | Sender's full name | Not Null |
| `receiver_name` | VARCHAR(100) | Receiver's full name | Not Null |
| `sender_phone` | VARCHAR(15) | Sender's phone number | Not Null |
| `receiver_phone` | VARCHAR(15) | Receiver's phone number | Not Null |
| `timestamp` | TIMESTAMP | Transaction creation time | Indexed, Not Null |
| `status` | VARCHAR(20) | Transaction status | `pending`/`failed`/`success` |
| `fraud_flag` | BOOLEAN | Fraud detection result | Default: false |
| `fraud_score` | FLOAT | Fraud probability score | 0.0 - 1.0 |

## 🧠 Fraud Detection

### Overview
The API includes a **machine learning-powered fraud detection system** that analyzes transaction patterns to identify suspicious activities.

### How It Works
1. **Training Data**: Model trained on historical transaction data
2. **Real-time Analysis**: Each transaction analyzed before completion
3. **Risk Scoring**: Probability score from 0.0 (safe) to 1.0 (suspicious)
4. **Automatic Blocking**: High-risk transactions automatically rejected

### Model Features
- **Algorithm**: Random Forest Classifier
- **Accuracy**: >99% on test data
- **Features**: Amount, UPI patterns, phone numbers, transaction frequency
- **Training**: Automated during Docker build process

### Integration
Fraud detection runs automatically when:
- Updating transaction status to "success"
- Processing transactions via `/process` endpoint

## 🏭 Production Deployment

### Gunicorn Configuration
The Docker setup uses Gunicorn with optimized settings:

```dockerfile
CMD ["gunicorn", "--bind", "0.0.0.0:8080", \
     "--workers", "4", \
     "--worker-class", "sync", \
     "--worker-connections", "1000", \
     "--timeout", "30", \
     "--keep-alive", "2", \
     "--max-requests", "1000", \
     "--max-requests-jitter", "50", \
     "run:app"]
```

### Environment Variables
```env
PORT=8080
DATABASE_URL=postgresql://user:password@host:5432/database
FLASK_ENV=production
```

### Scaling
```bash
# Scale application instances
docker-compose up -d --scale app=3

# Load balancing with nginx
# Configure nginx upstream for multiple app instances
```

## 🧪 Testing

### Run Database Tests
```bash
# Using Docker
docker-compose exec app python test/test_db.py

# Manual setup
uv run python test/test_db.py
```

### API Testing Examples
```bash
# Create transaction
curl -X POST http://localhost:8080/ \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 15000,
    "sender_upi_id": "test@upi",
    "receiver_upi_id": "merchant@upi",
    "sender_name": "Test User",
    "receiver_name": "Merchant",
    "sender_phone": "+919876543210",
    "receiver_phone": "+919876543211"
  }'

# Process transaction
curl -X POST http://localhost:8080/TXN1234567890ABCD/process
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation
- Ensure Docker builds pass

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Flask, SQLAlchemy, and scikit-learn
- Containerized with Docker
- Database migrations with Flask-Migrate
- Package management with uv

---

**Made with ❤️ for payment simulation and fraud detection research**

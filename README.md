# Payment Simulation API (Flask + PostgreSQL)

## 🚀 Overview
This project simulates payment transactions using Flask and PostgreSQL. It supports UPI-based sender/receiver flows, mule accounts, and full transaction logging.

---

## 🛠️ Installation & Setup

1. **Clone the repository:**
	```bash
	git clone <your-repo-url>
	cd payment_simulation
	```

2. **Install dependencies:**
	```bash
	uv pip install -e .
	```

3. **Configure environment:**
	- Edit `.env` with your PostgreSQL credentials:
	  ```env
	  PORT=5000
	  DATABASE_URL=postgresql://<user>:<password>@localhost:5432/<database>
	  ```

4. **Initialize database migrations:**
	```bash
	uv run flask --app run db init
	uv run flask --app run db migrate -m "Initial migration"
	uv run flask --app run db upgrade
	```

5. **Run the server:**
	```bash
	uv run python run.py
	```

---

## 🌐 API Endpoints

### Create Transaction
**POST /**
```json
{
  "amount": 25000.50,
  "sender_upi_id": "sender@upi",
  "receiver_upi_id": "mule@upi",
  "sender_name": "John Doe",
  "receiver_name": "Mule Account",
  "sender_phone": "+919876543210",
  "receiver_phone": "+919876543211"
}
```

### List All Transactions
**GET /**
Returns a list of all transactions.

### Get Transaction by ID
**GET /<transaction_id>**
Returns details for a specific transaction.

---

## 🏦 Database Schema
| Field           | Type         | Description                  |
|-----------------|--------------|------------------------------|
| id              | VARCHAR(50)  | Transaction ID (UUID)        |
| amount          | NUMERIC      | Amount (1 to 1 lakh)         |
| sender_upi_id   | VARCHAR(100) | Sender UPI ID                |
| receiver_upi_id | VARCHAR(100) | Receiver UPI ID (mule)       |
| sender_name     | VARCHAR(100) | Sender Name                  |
| receiver_name   | VARCHAR(100) | Receiver Name                |
| sender_phone    | VARCHAR(15)  | Sender Phone Number          |
| receiver_phone  | VARCHAR(15)  | Receiver Phone Number        |
| timestamp       | TIMESTAMP    | Transaction Timestamp        |

---

## 🖥️ Hosting Guide

1. **Production Setup:**
	- Use a production WSGI server (e.g., Gunicorn)
	- Set up environment variables securely
	- Ensure PostgreSQL is running and accessible

2. **Start with Gunicorn:**
	```bash
	uv pip install gunicorn
	gunicorn -w 4 run:app
	```

3. **Reverse Proxy (Optional):**
	- Use Nginx or Apache to proxy requests to Gunicorn

---

## 🧪 Testing
Run the included test script to verify database operations:
```bash
uv run python test/test_db.py
```

---

## 💡 Notes
- Make sure your PostgreSQL password is URL-encoded in `.env` if it contains special characters.
- For local development, you can use SQLite by changing the `DATABASE_URL`.
- All migrations and models are ready for production.
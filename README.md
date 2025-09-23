# Payment Simulation API (Flask + PostgreSQL)

## 🚀 Overview
This project simulate---

## 📁 Project Structure

```
payment_simulation/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── config/
│   │   ├── database.py      # Database configuration
│   │   └── envVars.py       # Environment variables
│   ├── models/
│   │   └── transactions.py  # Transaction model
│   └── routes/
│       ├── __init__.py
│       └── example.py       # API endpoints
├── migrations/              # Database migrations
├── Dockerfile               # Docker image
├── docker-compose.yml       # Production setup
├── docker-compose.dev.yml   # Development setup
├── pyproject.toml          # Python dependencies
├── run.py                  # Application entry point
└── README.md
```

---

## 🛠️ Manual Installation & Setupayment transactions using Flask and PostgreSQL. It supports UPI-based sender/receiver flows, mule accounts, and full transaction logging.

## 🐳 Docker Setup (Recommended)

### Quick Start with Docker Compose

1. **Clone and navigate to the project:**
   ```bash
   git clone https://github.com/samarth3301/payment-simulator.git
   cd payment_simulation
   ```

2. **Start all services:**
   ```bash
   docker-compose up -d
   ```

3. **Run database migrations:**
   ```bash
   docker-compose exec app uv run flask --app run db upgrade
   ```

4. **Access the API:**
   - API: http://localhost:8080
   - PostgreSQL: localhost:5432

### Docker Commands

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild and restart
docker-compose up --build -d

# Run database migrations
docker-compose exec app uv run flask --app run db upgrade

# Access PostgreSQL shell
docker-compose exec postgres psql -U webond -d webond

# Run tests
docker-compose exec app uv run python test_db.py
```

### Docker Environment Variables

The Docker setup uses `.env.docker` for configuration:

```env
PORT=8080
DATABASE_URL=
FLASK_ENV=production
```

### Docker Development Workflow

```bash
# Development with live reload
docker-compose -f docker-compose.dev.yml up

# Production deployment
docker-compose up -d

# View real-time logs
docker-compose logs -f app

# Scale the application
docker-compose up -d --scale app=3

# Clean up everything
docker-compose down -v --rmi all
```

---

## � Project Structure

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
	  PORT=8080
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

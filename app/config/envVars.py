import os
from dotenv import load_dotenv
from pathlib import Path

# Load from project root .env
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)

class Config:
    PORT = int(os.getenv("PORT", 5000))
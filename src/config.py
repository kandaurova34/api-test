import os
from dotenv import load_dotenv

load_dotenv()  # загружает переменные из .env


class Config:
    BASE_URL: str = os.getenv("BASE_URL", "http://localhost:8000")
    API_TIMEOUT: int = int(os.getenv("API_TIMEOUT", "5"))
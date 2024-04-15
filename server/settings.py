import os

DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = int(os.environ.get("DB_PORT", 5432))
DB_NAME = os.environ.get("DB_NAME", "dive")
DB_USERNAME = os.environ.get("DB_USERNAME", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "postgres")

BASE_API_URL = "https://newsapi.org/v2/everything"

NEWS_API_KEY="d4444c2e781f44faafe3564c9ec4cdc0"
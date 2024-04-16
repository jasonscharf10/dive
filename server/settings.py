import os

DB_URL = os.environ.get("DB_URL", "postgres://postgres:postgres@localhost:5432/dive")
BASE_API_URL = os.environ.get("BASE_API_URL", "https://newsapi.org/v2/everything")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY", "")

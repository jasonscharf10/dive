import os

DB_URL = os.environ.get("DB_URL", "postgres://postgres:postgres@localhost:5432/dive")
BASE_API_URL = "https://newsapi.org/v2/everything"
NEWS_API_KEY = "d4444c2e781f44faafe3564c9ec4cdc0"
import os

SERVER_API_BASE_URL = os.environ.get("SERVER_API_BASE_URL", "http://localhost:8080")
DB_URL = os.environ.get("DB_URL", "postgres://postgres:postgres@localhost:5432/dive")

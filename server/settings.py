import os

DB_URL = os.environ.get("DB_URL", "postgres://default:uDw0cybCWfe9@ep-lingering-king-a4nk4piq.us-east-1.aws.neon.tech:5432/verceldb?sslmode=require")
BASE_API_URL = os.environ.get("BASE_API_URL","https://newsapi.org/v2/everything")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY","d4444c2e781f44faafe3564c9ec4cdc0")

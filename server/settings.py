import os

DB_URL = os.environ.get("DB_URL", "postgres://postgres:postgres@localhost:5432/dive")
BASE_API_URL = os.environ.get("BASE_API_URL", "https://newsapi.org/v2/everything")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY", "")
SERVER_API_BASE_URL = os.environ.get("SERVER_API_BASE_URL", "http://localhost:8080")

REDDIT_CLIENT_ID = os.environ.get("REDDIT_CLIENT_ID", "_rbcUnfkFX6enVpa44HQ8Q")
REDDIT_CLIENT_SECRET = os.environ.get(
    "REDDIT_CLIENT_SECRET", "p2yPa5p0vEUxELpyfxgxmUYKLWqCrA"
)
REDDIT_PASSWORD = os.environ.get("REDDIT_PASSWORD", "Pandadoc10!")
REDDIT_USER_AGENT = os.environ.get(
    "REDDIT_USER_AGENT", "MyRedditApp v1.0 by National_Rhubarb9302"
)
REDDIT_USERNAME = os.environ.get("REDDIT_USERNAME", "National_Rhubarb9302")

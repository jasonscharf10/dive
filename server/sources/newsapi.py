import aiohttp
import asyncpg
from typing import Any


class NewsAPI:
    BASE_API_URL = "https://newsapi.org/v2/everything"
    _data: list[dict[str, Any]]

    async def request_data(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.BASE_API_URL
                + "?q=PandaDoc&from=2024-03-11&sortBy=publishedAt&apiKey=d4444c2e781f44faafe3564c9ec4cdc0"
            ) as response:
                data = await response.json(content_type=None)
                self._data = [
                    {
                        "title": item["title"],
                        "url": item["url"],
                        "publishedAt": item["publishedAt"],
                    }
                    for item in data["articles"]
                ]

    async def save_data(self):
        async with asyncpg.create_pool(
            host="localhost",
            port=5432,
            database="dive",
            user="postgres",
            password="postgres",
            command_timeout=60,
        ) as pool:
            async with pool.acquire() as conn:
                results = []
                for item in self._data:
                    result = await conn.fetchrow(
                        "insert into articles (title, url, published_date) values ($1,$2,$3) RETURNING *",
                        item["title"],
                        item["url"],
                        item["publishedAt"],
                    )
                    results.append(result)

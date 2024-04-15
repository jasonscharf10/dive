from typing import Any
import asyncpg
import settings


class DataSource:
    BASE_API_URL: str
    _data: list[dict[str, Any]]

    async def request_data(self):
        pass

    async def save_data(self):
        async with asyncpg.create_pool(
            dsn=settings.DB_URL,
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

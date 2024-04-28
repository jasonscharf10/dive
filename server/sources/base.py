from typing import Any
import asyncpg
import settings


class DataSource:
    _data: list[dict[str, Any]]
    _search_param: str

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
                        "insert into articles (title, url, published_date, source) values ($1,$2,$3,$4) RETURNING *",
                        item["title"],
                        item["url"],
                        item["publishedAt"],
                        item["source"],

                    )
                    results.append(result)

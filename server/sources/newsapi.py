import aiohttp
import asyncpg
from init_db import Database

class NewsAPI:
    BASE_API_URL = "https://newsapi.org/v2/everything"
    _data: list[dict[str]]

    async def call_api(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.BASE_API_URL
                + "?q=PandaDoc&from=2024-03-05&sortBy=publishedAt&apiKey=d4444c2e781f44faafe3564c9ec4cdc0"
            ) as response:
                _data = await response.json()
                articles = _data["articles"]
                _data = [
                    {
                        "title": item["title"],
                        "url": item["url"],
                        "publishedAt": item["publishedAt"],
                    }
                    for item in articles
                ]
                #print(_data)
                return _data
            
    async def insert_rows(self):
        _data = await self.call_api()
        # results = []
        # for item in _data:
        #     print(item["title"])
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
                for item in _data:
                    result = await conn.fetchrow(
                        "insert into articles (title, url, published_date) values ($1,$2,$3) RETURNING *", item["title"], item["url"], item["publishedAt"]
                    )
                    results.append(result)
                    print(results)

        # if result:
        #     output = [result]
        # else:
        #     output = []

        # print(output)

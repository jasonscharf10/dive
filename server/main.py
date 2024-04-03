# Server
import asyncio
import aiohttp
from aiohttp import web
import asyncpg
import pandas as pd
from pandas import json_normalize

from init_db import Database
from sources.base import Base
from sources.newsapi import NewsAPI


class News:
    def __init__(self, title, url, published_date, api_url):
        self.title = title
        self.url = url
        self.published_date = published_date
        self.api_url = api_url


async def handle(request):
    query = request.match_info.get("query", "Anonymous")
    query = "PandaDoc"

    async with aiohttp.ClientSession() as session:
        url = f"https://newsapi.org/v2/everything?q={query}&from=2024-02-28&sortBy=publishedAt&apiKey=d4444c2e781f44faafe3564c9ec4cdc0"
        async with session.get(url) as response:
            data = await response.json()
            df = json_normalize(data, "articles")
            df = df.reset_index()
            # df['publishedAt'].apply(lambda x: x.toordinal())
            print(df["title"])

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
            for index, row in df.iterrows():
                result = await conn.fetchrow(
                    "insert into news (title,url,published_date) values ($1,$2,$3) RETURNING *",
                    row["title"],
                    row["url"],
                    row["publishedAt"],
                )
                results.append(result)

    ### Need to fix ###
    if result:
        data = [result]
    else:
        data = []

    return web.json_response(data)


async def main():
    # database = Database()
    # news_api = Base(
    #     "https://newsapi.org/v2/everything?q=PandaDoc&from=2024-02-28&sortBy=publishedAt&apiKey=d4444c2e781f44faafe3564c9ec4cdc0"
    # )
    # print("main")
    # await database.setup()
    news_api = NewsAPI()
    #news_result = await news_api.call_api()
    # print(news_result)
    new_rows = await news_api.insert_rows()
    #print(new_rows)
    # print(news_result)
    # print(insert_rows)


app = web.Application()
# http://localhost:8080/ --- first request
# http://localhost:8080/TEST --- second request
app.add_routes([web.get("/", handle), web.get("/{query}", handle)])

if __name__ == "__main__":
    asyncio.run(main())
    web.run_app(app)

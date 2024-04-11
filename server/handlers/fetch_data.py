import aiohttp
import asyncpg
from aiohttp import web


async def fetch_data(request):
    """docstring"""
    async with asyncpg.create_pool(
        host="localhost",
        port=5432,
        database="dive",
        user="postgres",
        password="postgres",
        command_timeout=60,
    ) as pool:
        async with pool.acquire() as conn:
            result = await conn.fetch("""SELECT * from articles""")

    if result:
        data = [
            {
                "id": item["id"],
                "title": item["title"],
                "url": item["url"],
                "published_date": item["published_date"],
            }
            for item in result
        ]
    else:
        data = []

    return web.json_response(data)

import asyncpg
from aiohttp import web
import settings
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)


async def save_data(request):
    try:
        data = await request.json()
        logging.info("Received data: %s", data)

        async with asyncpg.create_pool(dsn=settings.DB_URL, command_timeout=60) as pool:
            async with pool.acquire() as conn:
                for item in data:
                    logging.info("Saving item: %s", item)
                    published_date = (
                        datetime.fromisoformat(item["published_date"]).date()
                        if item["published_date"]
                        else None
                    )
                    await conn.execute(
                        """
                        INSERT INTO articles (search_param, title, url, published_date, source)
                        VALUES ($1, $2, $3, $4, $5)
                        ON CONFLICT (url) DO NOTHING
                        """,
                        item["search_param"],
                        item["title"],
                        item["url"],
                        published_date,
                        item["source"],
                    )
        return web.Response(text="Data saved", status=200)

    except Exception as e:
        logging.error("Error saving data: %s", str(e))
        return web.Response(text="Internal Server Error", status=500)

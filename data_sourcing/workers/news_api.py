import asyncio
import asyncpg
import settings
from sources.newsapi import NewsAPI
import logging


async def fetch_user_input():
    async with asyncpg.create_pool(dsn=settings.DB_URL) as pool:
        async with pool.acquire() as conn:
            result = await conn.fetchrow(
                "SELECT search_param FROM user_inputs ORDER BY id DESC LIMIT 1"
            )
            if result:
                return result["search_param"]
            return None


async def news_api_worker():
    delay_time = 5  # seconds

    while True:
        search_param = await fetch_user_input()
        if not search_param:
            logging.info("No user input found, skipping data fetch.")
            return
        print(f"Running *News API* worker for {search_param}")
        logging.info("Starting data fetch with search_param: %s", search_param)
        news_api = NewsAPI(search_param)
        news_api._search_param = search_param
        await news_api.request_data()
        await news_api.save_data()
        logging.info("Data fetch and update complete.")

        print("Worker *News API* waiting")
        await asyncio.sleep(delay_time)

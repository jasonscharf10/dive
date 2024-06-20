import asyncio
import asyncpg
import settings
from sources.redditapi import RedditAPI
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


async def reddit_api_worker():
    search_param = await fetch_user_input()
    if not search_param:
        logging.info("No user input found, skipping data fetch.")
        return

    delay_time = 5  # seconds

    while True:
        print(f"Running *Reddit API* worker for {search_param}")
        logging.info("Starting data fetch with search_param: %s", search_param)

        reddit_api = RedditAPI()
        reddit_api._search_param = search_param
        await reddit_api.request_data()
        await reddit_api.save_data()
        logging.info("Data fetch and update complete.")

        print("Worker *Reddit API* waiting")
        await asyncio.sleep(delay_time)

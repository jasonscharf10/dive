import asyncio
import aiohttp
import settings
from sources.redditapi import RedditAPI
import logging


async def fetch_user_input():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{settings.SERVER_API_BASE_URL}/fetch-user-input") as response:
            if response.status == 200:
                data = await response.json()
                return data.get("search_param")
            else:
                logging.error("Error fetching user input: %s", response.status)
                return None


async def reddit_api_worker():
    delay_time = 5  # seconds

    while True:
        search_param = await fetch_user_input()
        if not search_param:
            logging.info("No user input found, skipping data fetch.")
            return

        print(f"Running *Reddit API* worker for {search_param}")
        logging.info("Starting data fetch with search_param: %s", search_param)

        reddit_api = RedditAPI()
        reddit_api._search_param = search_param
        await reddit_api.request_data()
        await reddit_api.save_data()
        logging.info("Data fetch and update complete.")

        print("Worker *Reddit API* waiting")
        await asyncio.sleep(delay_time)

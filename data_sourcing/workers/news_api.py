import asyncio
import aiohttp
import settings
from sources.newsapi import NewsAPI
import logging


async def fetch_user_input():
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.get(f"{settings.SERVER_API_BASE_URL}/fetch-user-input") as response:
            if response.status == 200:
                data = await response.json()
                return data.get("search_param")
            else:
                logging.error("Error fetching user input: %s", response.status)
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
        news_api = NewsAPI()
        news_api._search_param = search_param
        await news_api.request_data()
        await news_api.save_data()
        logging.info("Data fetch and update complete.")

        print("Worker *News API* waiting")
        await asyncio.sleep(delay_time)

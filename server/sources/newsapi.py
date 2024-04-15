import aiohttp
import asyncpg
from typing import Any
import settings
from datetime import date
from dateutil.relativedelta import relativedelta
from sources.base import DataSource

class NewsAPI(DataSource):
    async def request_data(self):
        one_month_before = date.today() + relativedelta(months=-1)
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{settings.BASE_API_URL}?q=PandaDoc&from={one_month_before}&sortBy=publishedAt&apiKey={settings.NEWS_API_KEY}"
            ) as response:
                data = await response.json(content_type=None)
                self._data = [
                    {
                        "title": item["title"],
                        "url": item["url"],
                        "publishedAt": item["publishedAt"],
                    }
                    for item in data["articles"]
                ]

    

from datetime import date
import aiohttp
from dateutil import parser
from dateutil.relativedelta import relativedelta
from sources.base import DataSource
import settings


class NewsAPI(DataSource):
    async def request_data(self):
        one_month_before = date.today() + relativedelta(months=-1)
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{settings.BASE_API_URL}?q={self._search_param}&from={one_month_before}&sortBy=publishedAt&apiKey={settings.NEWS_API_KEY}"
            ) as response:
                data = await response.json(content_type=None)
                self._data = [
                    {
                        "search_param": self._search_param,
                        "title": item["title"],
                        "url": item["url"],
                        "published_date": parser.parse(item["publishedAt"]).date(),
                        "source": "NewsAPI",
                    }
                    for item in data["articles"]
                ]

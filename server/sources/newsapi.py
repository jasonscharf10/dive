from datetime import date
import aiohttp
from dateutil.relativedelta import relativedelta
from sources.base import DataSource
import streamlit as st


class NewsAPI(DataSource):
    async def request_data(self):
        one_month_before = date.today() + relativedelta(months=-1)
        BASE_API_URL = st.secrets["BASE_API_URL"]
        NEWS_API_KEY = st.secrets["NEWS_API_KEY"]
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{BASE_API_URL}?q=PandaDoc&from={one_month_before}&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
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

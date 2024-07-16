from typing import Any
import aiohttp
import settings
from datetime import date


class DataSource:
    _data: list[dict[str, Any]]
    _search_param: str

    async def request_data(self):
        pass

    def serialize_data(self):
        for item in self._data:
            if isinstance(item.get("published_date"), date):
                item["published_date"] = item["published_date"].isoformat()

    async def save_data(self):
        self.serialize_data()
        async with aiohttp.ClientSession() as session:
            url = f"{settings.SERVER_API_BASE_URL}/save-data"
            async with session.post(url, json=self._data) as response:
                response_text = await response.text()
                print(response_text)

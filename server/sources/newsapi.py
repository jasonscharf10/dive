import aiohttp


class NewsAPI:
    BASE_API_URL = "https://newsapi.org/v2/everything"
    _data: list[dict[str]]

    async def call_api(self):
        BASE_API_URL = self.BASE_API_URL
        async with aiohttp.ClientSession() as session:
            async with session.get(
                BASE_API_URL
                + "?q=PandaDoc&from=2024-03-05&sortBy=publishedAt&apiKey=d4444c2e781f44faafe3564c9ec4cdc0"
            ) as response:
                _data = await response.json()
                articles = _data["articles"]
                _data = [
                    {
                        "title": item["title"],
                        "url": item["url"],
                        "publishedAt": item["publishedAt"],
                    }
                    for item in articles
                ]
                print(_data)
                return _data

                # return json_data

    # def parse_data(self):
    #     url = self.api_url
    #     news_api = Base.api_call(self)
    #     print(news_api)

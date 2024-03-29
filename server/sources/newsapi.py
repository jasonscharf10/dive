from sources.base import Base
from pandas import json_normalize


class NewsAPI:
    async def parse_data(self):
        news_api = Base("https://newsapi.org/v2/everything?q=PandaDoc&from=2024-02-29&sortBy=publishedAt&apiKey=d4444c2e781f44faafe3564c9ec4cdc0")
        data = await news_api.api_call()
        df = json_normalize(data, "articles")
        df = df.reset_index()
        print("news class")
        return df
        
        
    # def parse_data(self):
    #     url = self.api_url
    #     news_api = Base.api_call(self)
    #     print(news_api)

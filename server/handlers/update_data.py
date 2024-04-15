import aiohttp
from aiohttp import web
from sources.newsapi import NewsAPI


async def update_data(request):
    """docstring"""
    news_api = NewsAPI()
    await news_api.request_data()
    await news_api.save_data()
    return web.Response(text="Data updated successfully")

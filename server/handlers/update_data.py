from aiohttp import web
from sources.newsapi import NewsAPI
from sources.redditapi import RedditAPI


async def update_data(request):
    """docstring"""
    search_param = request.query.get("search_param")
    if not search_param:
        return web.Response(text="Search parameter is missing.", status=400)
    news_api = NewsAPI()
    news_api._search_param = search_param
    reddit_api = RedditAPI()
    reddit_api._search_param = search_param
    print(search_param)
    await reddit_api.request_data()
    await reddit_api.save_data()
    await news_api.request_data()
    await news_api.save_data()
    return web.Response(text="Data updated successfully")

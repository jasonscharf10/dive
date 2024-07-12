import asyncio
from aiohttp import web
from workers.news_api import news_api_worker
from workers.reddit_api import reddit_api_worker
from sanic import Sanic
from sanic.response import json

app = Sanic("Data-Sourcing")
 

@app.route('/')
async def index(request):
    tasks = [
    asyncio.create_task(news_api_worker()),
    asyncio.create_task(reddit_api_worker())
    ]
    await asyncio.gather(*tasks)
    return json({"status": "tasks started"})

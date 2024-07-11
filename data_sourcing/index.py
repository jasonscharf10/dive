import asyncio
from aiohttp import web
from workers.news_api import news_api_worker
from workers.reddit_api import reddit_api_worker
from sanic import Sanic, json, text

app = Sanic("Data-Sourcing")
 
@app.route('/')
async def index(request, path=""):
    return json({'hello': path})

@app.route('/run_tasks')
async def run_tasks(request):
    tasks = [
        asyncio.create_task(news_api_worker()),
        asyncio.create_task(reddit_api_worker())
    ]
    await asyncio.gather(*tasks)
    return text("Tasks started")
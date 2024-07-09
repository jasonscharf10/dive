import asyncio
import asyncpg
from aiohttp import web
import settings
from workers.news_api import news_api_worker
from workers.reddit_api import reddit_api_worker

async def run_tasks(request):
    tasks = []
    tasks.append(asyncio.create_task(news_api_worker()))
    tasks.append(asyncio.create_task(reddit_api_worker()))

    await asyncio.gather(*tasks)

    return web.Response(text="Tasks completed", status=200)

app = web.Application()
app.add_routes([web.get('/', run_tasks)])

if __name__ == "__main__":
    web.run_app(app)
else:
    asgi_app = app
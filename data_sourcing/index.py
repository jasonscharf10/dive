import asyncio
from aiohttp import web
from aiohttp_asgiref import ASGIApplication
import settings
from workers.news_api import news_api_worker
from workers.reddit_api import reddit_api_worker

async def run_tasks(request):
    tasks = [
        asyncio.create_task(news_api_worker()),
        asyncio.create_task(reddit_api_worker())
    ]
    await asyncio.gather(*tasks)
    return web.Response(text="Tasks completed", status=200)

app = web.Application()
app.add_routes([web.get('/', run_tasks)])

# Wrap the aiohttp app with aiohttp-asgiref for ASGI compatibility
asgi_app = ASGIApplication(app)

if __name__ == "__main__":
    web.run_app(app)
else:
    app = asgi_app

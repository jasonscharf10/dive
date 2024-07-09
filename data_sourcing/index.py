import asyncio
from aiohttp import web
import settings
from workers.news_api import news_api_worker
from workers.reddit_api import reddit_api_worker
from aiohttp_asgi import ASGIApplication

async def run_tasks(request):
    tasks = [
        asyncio.create_task(news_api_worker()),
        asyncio.create_task(reddit_api_worker())
    ]
    await asyncio.gather(*tasks)
    return web.Response(text="Tasks completed", status=200)

app = web.Application()
app.add_routes([web.get('/', run_tasks)])

# Wrap the aiohttp app with aiohttp-asgi for ASGI compatibility
asgi_app = ASGIApplication(app)

if __name__ == "__main__":
    web.run_app(app)
else:
    app = asgi_app
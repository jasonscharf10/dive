import asyncio
import logging
from aiohttp import web
from asgiref.compatibility import guarantee_single_callable
from asgiref.wsgi import WsgiToAsgi
from workers.news_api import news_api_worker
from workers.reddit_api import reddit_api_worker

logging.basicConfig(level=logging.INFO)

async def run_background_tasks():
    tasks = [
        news_api_worker(),
        reddit_api_worker()
    ]
    await asyncio.gather(*tasks)

async def start_background_tasks(app):
    app['background_tasks'] = asyncio.create_task(run_background_tasks())

async def stop_background_tasks(app):
    app['background_tasks'].cancel()
    await app['background_tasks']

async def handle(request):
    return web.Response(text="Background tasks are running.")

app = web.Application()
app.add_routes([web.get('/', handle)])
app.on_startup.append(start_background_tasks)
app.on_cleanup.append(stop_background_tasks)

# Make sure Vercel treats this as an ASGI app
asgi_app = WsgiToAsgi(guarantee_single_callable(app))

if __name__ == "__main__":
    web.run_app(app)
else:
    import os
    import uvicorn

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(asgi_app, host=host, port=port)

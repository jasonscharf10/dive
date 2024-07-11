import asyncio
from aiohttp import web
from workers.news_api import news_api_worker
from workers.reddit_api import reddit_api_worker

async def run_tasks(request):
    tasks = [
        asyncio.create_task(news_api_worker()),
        asyncio.create_task(reddit_api_worker())
    ]
    await asyncio.gather(*tasks)
    return web.Response(text="Tasks started")

app = web.Application()
app.router.add_get("/", run_tasks)

# Make the app visible to Vercel
if __name__ == "__main__":
    web.run_app(app)
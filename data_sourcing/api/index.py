import asyncio
from workers.news_api_worker import news_api_worker
from workers.reddit_api_worker import reddit_api_worker

async def main():
    tasks = [
        news_api_worker(),
        reddit_api_worker()
    ]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
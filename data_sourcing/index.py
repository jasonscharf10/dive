from http.server import BaseHTTPRequestHandler
import asyncio
import asyncpg
import settings
from workers.news_api import news_api_worker
from workers.reddit_api import reddit_api_worker


# async def main():
#     tasks = []

#     tasks.append(asyncio.create_task(news_api_worker()))
#     tasks.append(asyncio.create_task(reddit_api_worker()))

#     await asyncio.gather(*tasks)


# if __name__ == "__main__":
#     asyncio.run(main())

class handler(BaseHTTPRequestHandler):
  tasks=[]

  async def do_GET(self):
    self.send_response(200)
    self.send_header('Content-type', 'text/plain')
    self.end_headers()
    self.tasks.append(asyncio.create_task(news_api_worker()))
    self.tasks.append(asyncio.create_task(reddit_api_worker()))
    await asyncio.gather(*self.tasks)
    return
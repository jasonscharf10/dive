import aiohttp
from init_db import Database
import asyncio
from aiohttp import web
import asyncpg


class Base:
    async def api_call(self, api_url):
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                data = await response.json()
                print("base class")
                return data

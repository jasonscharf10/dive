import asyncpg
from aiohttp import web
import logging
import settings

logging.basicConfig(level=logging.INFO)


async def fetch_user_input(request):
    try:
        async with asyncpg.create_pool(dsn=settings.DB_URL) as pool:
            async with pool.acquire() as conn:
                result = await conn.fetchrow(
                    "SELECT search_param FROM user_inputs ORDER BY id DESC LIMIT 1"
                )
                if result:
                    return web.json_response({"search_param": result["search_param"]})
                return web.json_response({"search_param": None})
    except Exception as e:
        logging.error("Error fetching user input: %s", str(e))
        return web.Response(text="Internal Server Error", status=500)

import asyncpg
from aiohttp import web
import settings


async def fetch_data(request):
    """docstring"""
    search_param = request.query.get("search_param")
    print(search_param)
    async with asyncpg.create_pool(
        dsn=settings.DB_URL,
        command_timeout=60,
    ) as pool:
        async with pool.acquire() as conn:
            result = await conn.fetch(
                """
                SELECT * FROM articles 
                WHERE search_param ILIKE $1 
                ORDER BY published_date DESC
                """,
                search_param,
            )

    if result:
        data = [
            {
                "id": item["id"],
                "search_param": item["search_param"],
                "title": item["title"],
                "url": item["url"],
                "published_date": item["published_date"].isoformat(),
                "source": item["source"],
            }
            for item in result
        ]
    else:
        data = []

    return web.json_response(data)

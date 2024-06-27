import asyncpg
from aiohttp import web
import settings


async def save_user_input(request):
    data = await request.json()
    search_param = data.get("search_param")
    print(search_param)
    if not search_param:
        return web.Response(text="Invalid input", status=400)
    async with asyncpg.create_pool(
        dsn=settings.DB_URL,
        command_timeout=60,
    ) as pool:
        async with pool.acquire() as conn:
            await conn.execute(
                """
                    INSERT INTO user_inputs (search_param)
                VALUES ($1)
            """,
                search_param,
            )
    return web.Response(text="Input saved", status=200)

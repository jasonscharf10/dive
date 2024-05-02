# Server
import asyncio
from aiohttp import web

from init_db import Database
from handlers.fetch_data import fetch_data
from handlers.update_data import update_data


async def main():
    database = Database()
    await database.setup()


app = web.Application()

app.add_routes(
    [
        web.post("/update-data", update_data),
        web.get("/fetch-data", fetch_data),
    ]
)

if __name__ == "__main__":
    asyncio.run(main())
    web.run_app(app)

import asyncpg
from init_db import Database


async def insert_rows(df):
    database = Database()
    async with asyncpg.create_pool(database) as pool:
        async with pool.acquire() as conn:
            results = []
            for index, row in df.iterrows():
                result = await conn.fetchrow(
                    "insert into news (title,url,published_date) values ($1,$2,$3) RETURNING *",
                    row["title"],
                    row["url"],
                    row["publishedAt"],
                )
                results.append(result)
                print("insert rows")

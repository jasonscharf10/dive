import asyncpg


class Database:
    db_host = "localhost"
    db_port = 5432
    db_name = "dive"
    db_username = "postgres"
    db_password = "postgres"

    async def setup(self):
        """docstring"""
        async with asyncpg.create_pool(
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
            user=self.db_username,
            password=self.db_password,
            command_timeout=60,
        ) as pool:
            async with pool.acquire() as conn:
                await conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS articles (
                        id serial PRIMARY KEY,
                        title varchar NULL,
                        url varchar NULL,
                        published_date varchar NULL
                    )
                """
                )

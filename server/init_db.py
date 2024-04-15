import asyncpg
import streamlit as st


class Database:
    db_url = st.secrets["DB_URL"]

    async def setup(self):
        """docstring"""
        async with asyncpg.create_pool(
            dsn=self.db_url,
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
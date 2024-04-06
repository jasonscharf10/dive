# Client
import asyncio
import aiohttp
import streamlit as st


async def main():
    """docstring"""
    async with aiohttp.ClientSession() as session:
        search = st.text_input("Search Input")
        if search:
            url = f"https://newsapi.org/v2/everything?q={search}&from=2024-02-26&sortBy=publishedAt&apiKey=d4444c2e781f44faafe3564c9ec4cdc0"
            async with session.get(url) as response:
                data = await response.json()
                st.title("Search Results")
                st.write(data)


if __name__ == "__main__":
    asyncio.run(main())

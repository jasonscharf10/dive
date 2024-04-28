# Client
import asyncio

import aiohttp

import streamlit as st
import pandas as pd
import altair as alt
import settings


async def load_data(should_force_load: bool = False):
    if should_force_load or "chart_data" not in st.session_state:
        url = f"{settings.SERVER_API_BASE_URL}/fetch-data"
        async with aiohttp.ClientSession(trust_env=True) as session:
            async with session.get(url) as response:
                data = await response.json()
                st.session_state["chart_data"] = pd.DataFrame(
                    {
                        "title": [item["title"] for item in data],
                        "url": [item["url"] for item in data],
                        "published_date": [item["published_date"] for item in data],
                        "source": [item["source"] for item in data],
                    }
                )
                print(st.session_state)

# def text_input():
#     result = st.text_input('Search parameter')
#     return result

async def main():
    """docstring"""
    st.title("PandaDoc News Articles")
    search_param = st.text_input('Search parameter')
    await load_data()
    if st.button("Refresh Data"):
        url = f"{settings.SERVER_API_BASE_URL}/update-data"
        async with aiohttp.ClientSession(trust_env=True) as session:
            async with session.post(url, params={"search_param": search_param}) as response:
                text = response.text
                await load_data(should_force_load=True)
    st.write(st.session_state["chart_data"])
    c = (
        alt.Chart(st.session_state["chart_data"])
        .mark_bar()
        .encode(x="published_date", y="count()")
    )
    st.altair_chart(c, use_container_width=True)


if __name__ == "__main__":
    asyncio.run(main())

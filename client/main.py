# Client
import asyncio

import aiohttp

import settings

import streamlit as st
import pandas as pd


async def save_user_input(search_param):
    async with aiohttp.ClientSession(trust_env=True) as session:
        url = f"{settings.SERVER_API_BASE_URL}/save-user-input"
        async with session.post(url, json={"search_param": search_param}) as response:
            response_text = await response.text()
            print(response_text)


async def load_data(search_param, should_force_load: bool = False):
    if should_force_load or "chart_data" not in st.session_state:
        url = f"{settings.SERVER_API_BASE_URL}/fetch-data"
        async with aiohttp.ClientSession(trust_env=True) as session:
            async with session.get(
                url, params={"search_param": search_param}
            ) as response:
                data = await response.json(content_type=None)
                print(data)
                st.session_state["chart_data"] = pd.DataFrame(
                    {
                        "search_param": [item["search_param"] for item in data],
                        "title": [item["title"] for item in data],
                        "url": [item["url"] for item in data],
                        "published_date": [item["published_date"] for item in data],
                        "source": [item["source"] for item in data],
                    }
                )
                st.session_state["chart_data"].fillna("None", inplace=True)


async def main():
    """docstring"""
    st.title("News Articles Sentiment Analysis")
    search_param = st.text_input("Search parameter")
    await load_data(search_param)
    if st.button("Refresh Data"):
        await save_user_input(search_param)
        await load_data(search_param, should_force_load=True)
    st.dataframe(
        st.session_state["chart_data"],
        use_container_width=True,
        hide_index=True,
        column_config={
            "url": st.column_config.LinkColumn(
                "Link URL",
                display_text="View Link",
            )
        },
    )


if __name__ == "__main__":
    asyncio.run(main())

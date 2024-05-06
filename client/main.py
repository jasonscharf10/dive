# Client
import asyncio

import aiohttp

import streamlit as st
import pandas as pd
import altair as alt
import settings


async def load_data(search_param, should_force_load: bool = False):
    if should_force_load or "chart_data" not in st.session_state:
        url = f"{settings.SERVER_API_BASE_URL}/fetch-data"
        async with aiohttp.ClientSession(trust_env=True) as session:
            async with session.get(
                url, params={"search_param": search_param}
            ) as response:
                data = await response.json(content_type=None)
                st.session_state["chart_data"] = pd.DataFrame(
                    {
                        "search_param": [item["search_param"] for item in data],
                        "title": [item["title"] for item in data],
                        "url": [item["url"] for item in data],
                        "published_date": [item["published_date"] for item in data],
                        "source": [item["source"] for item in data],
                    }
                )


async def main():
    """docstring"""
    st.title("Latest News Articles")
    search_param = st.text_input("Search parameter")
    await load_data(search_param)
    if st.button("Refresh Data"):
        url = f"{settings.SERVER_API_BASE_URL}/update-data"
        async with aiohttp.ClientSession(trust_env=True) as session:
            async with session.post(
                url, params={"search_param": search_param}
            ) as response:
                text = response.text
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
    c = (
        alt.Chart(st.session_state["chart_data"])
        .mark_bar()
        .encode(x="published_date", y="count()")
    )
    st.altair_chart(c, use_container_width=True)


if __name__ == "__main__":
    asyncio.run(main())

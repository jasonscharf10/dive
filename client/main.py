# Client
import asyncio

import aiohttp

import streamlit as st
import pandas as pd
import altair as alt


async def main():
    """docstring"""
    st.title("PandaDoc News Articles")
    if st.button("Refresh Data"):
        url = "http://15.204.162.212:8501/update-data"
        async with aiohttp.ClientSession(trust_env=True) as session:
            async with session.post(url) as response:
                text = response.text
                url = "http://15.204.162.212:8501/fetch-data"
                async with session.get(url) as response:
                    data = await response.json()
                    chart_data = pd.DataFrame(
                        {
                            "title": [item["title"] for item in data],
                            "url": [item["url"] for item in data],
                            "published_date": [item["published_date"] for item in data],
                        }
                    )
                    st.write(chart_data)
                    c = (
                        alt.Chart(chart_data)
                        .mark_bar()
                        .encode(x="published_date", y="count()")
                    )
                    st.altair_chart(c, use_container_width=True)


if __name__ == "__main__":
    asyncio.run(main())

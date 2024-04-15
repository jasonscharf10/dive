# Client
import asyncio

import aiohttp

import streamlit as st
import pandas as pd
import altair as alt


async def main():
    """docstring"""
    if st.button("Refresh Data"):
        url = "https://kfqooscp7vt8bxq87g6t2h.streamlit.app/update-data"
        async with aiohttp.ClientSession() as session:
            async with session.post(url) as response:
                text = response.text
                url = "https://kfqooscp7vt8bxq87g6t2h.streamlit.app/fetch-data"
                async with session.get(url) as response:
                    data = await response.json()
                    st.title("First Streamlit Test App")
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

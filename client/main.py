# Client
import asyncio

import aiohttp

import streamlit as st

async def main():
    """docstring"""
    async with aiohttp.ClientSession() as session:
        if st.button("Refresh Data"):
            url = "http://localhost:8080/update-data"
            async with session.post(url) as response:
                text=response.text
                print(text)
                url = "http://localhost:8080/fetch-data"
                async with session.get(url) as response:
                    data = await response.json()
                    st.title("First Streamlit Test App")
                    st.write(data)
                # chart_data = pd.DataFrame(
                #     {
                #         "title": [item["title"] for item in data],
                #         "url": [item["url"] for item in data],
                #         "published_date": [item["publishedAt"] for item in data],
                #     }
                # )
                # st.write(chart_data)
            # c = alt.Chart(chart_data).mark_bar().encode(x="url", y="count()")
            # st.altair_chart(c, use_container_width=True)
            # st.bar_chart(chart_data, x="url", y="name")


if __name__ == "__main__":
    asyncio.run(main())

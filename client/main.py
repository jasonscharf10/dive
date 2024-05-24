# Client
import asyncio

import aiohttp

import streamlit as st
import pandas as pd
import altair as alt
import settings

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

nltk.download("all")


def preprocess_text(text):

    # Tokenize the text

    tokens = word_tokenize(text.lower())

    # Remove stop words

    filtered_tokens = [
        token for token in tokens if token not in stopwords.words("english")
    ]

    # Lemmatize the tokens

    lemmatizer = WordNetLemmatizer()

    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]

    # Join the tokens back into a string

    processed_text = " ".join(lemmatized_tokens)

    return processed_text


analyzer = SentimentIntensityAnalyzer()


# create get_sentiment function


def get_sentiment(text):

    scores = analyzer.polarity_scores(text)

    sentiment = scores["compound"]

    return sentiment


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
                st.session_state["chart_data"]["title"] = st.session_state[
                    "chart_data"
                ]["title"].apply(preprocess_text)
                # apply get_sentiment function
                st.session_state["chart_data"]["sentiment"] = st.session_state[
                    "chart_data"
                ]["title"].apply(get_sentiment)


async def main():
    """docstring"""
    st.title("News Articles Sentiment Analysis")
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
    avg_sentiment = st.session_state["chart_data"].loc[:, "sentiment"].mean()
    st.write(
        "The Average Sentiment for " + str(search_param) + " is " + str(avg_sentiment)
    )
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
        .encode(x="published_date", y="mean(sentiment)")
    )
    st.altair_chart(c, use_container_width=True)


if __name__ == "__main__":
    asyncio.run(main())

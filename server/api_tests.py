from datetime import date

import unittest
from unittest import TestCase

import aiohttp
from dateutil.relativedelta import relativedelta
import streamlit as st


class IntegrationTests(TestCase):
    async def test_status_codes_200(self):
        one_month_before = date.today() + relativedelta(months=-1)
        BASE_API_URL = st.secrets["BASE_API_URL"]
        NEWS_API_KEY = st.secrets["NEWS_API_KEY"]
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{BASE_API_URL}?q=PandaDoc&from={one_month_before}&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
            ) as response:
                assert response.status_code == 200


if __name__ == "__main__":
    unittest.main()

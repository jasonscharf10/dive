import unittest
from unittest import TestCase

import aiohttp
import settings
from datetime import date
from dateutil.relativedelta import relativedelta

class IntegrationTests(TestCase):
    async def test_status_codes_200(self):
        one_month_before = date.today() + relativedelta(months=-1)
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{settings.BASE_API_URL}?q=PandaDoc&from={one_month_before}&sortBy=publishedAt&apiKey={settings.NEWS_API_KEY}"
            ) as response:
                assert response.status_code == 200

if __name__ == "__main__":
    unittest.main()
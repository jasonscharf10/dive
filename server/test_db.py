import unittest
from handlers.fetch_data import fetch_data
from aiohttp.test_utils import AioHTTPTestCase
from aiohttp import web


class TestApp(AioHTTPTestCase):
    async def get_application(self):
        # Define and return the aiohttp application for testing
        app = web.Application()
        app.router.add_get("/fetch_data", fetch_data)
        return app

    async def test_fetch_data_with_data(self):
        # Make a request to the fetch_data endpoint
        resp = await self.client.get("/fetch_data")

        # Check if the response status is 200 OK
        # self.assertEqual(resp.status, 200)

        # Check if the response data matches the expected format
        data = await resp.json()
        # self.assertEqual(len(data), 2)
        self.assertEqual(
            data[0]["title"],
            "Mike Breen opens up about rare double ‘Bang’ call for Donte DiVincenzo’s heroic Knicks 3-pointer",
        )
        # self.assertEqual(data[1]["title"], "Test Article 2")


if __name__ == "__main__":
    unittest.main()

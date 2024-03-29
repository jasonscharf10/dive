import aiohttp


class Base:
    def __init__(self, api_url):
        self.api_url = api_url

    async def api_call(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.api_url) as response:
                data = await response.json()
                print("base class")
                return data

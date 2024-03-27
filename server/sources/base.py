import aiohttp


class Base:
    def __init__(self, api_url):
        self.api_url = api_url

    async def api_call(self):
        async with aiohttp.ClientSession() as session:
            url = self.api_url
            async with session.get(url) as response:
                data = await response.json()
                print(data)

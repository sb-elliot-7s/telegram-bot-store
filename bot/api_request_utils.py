import aiohttp


class APIRequest:
    @staticmethod
    async def api_request(url: str, headers: dict = None, query_params: dict = None):
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url=url, params=query_params) as response:
                if response.status == 200:
                    return await response.json()

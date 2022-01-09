import json
import aiohttp
import asyncio

from API.requests import Requests


class RequestsAsync(Requests):
    def __init__(self, Authorization:str):
        self.headers = {"Authorization":f"token {Authorization}"}

    async def get(self, url, mapper, **kwargs):
        params = kwargs
        headers = {'Accept': 'application/vnd.github.v3+json'}
        async with aiohttp.ClientSession() as session:
            async with session.get(url,
                                   headers=self.headers,
                                   params=params) as response:
                result = await mapper(response)
        return result
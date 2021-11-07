import requests
from . import auth

import asyncio
import aiohttp
import oauthlib.oauth1


class APIRequest():
    def __init__(self) -> None:
        self.type = 'API_Requester'

    def org_request(self, last_id):
        return requests.get(f'https://api.github.com/organizations'
            f'?since={last_id}&per_page=100', auth=auth.auth())

    def repos_request(self, org_name, page):
        return requests.get(f'https://api.github.com/orgs/{org_name}'
            f'/repos?per_page=100&page={page}', auth=auth.auth())


class AsyncAPIRequest(APIRequest):
    def __init__(self) -> None:
        super().__init__()
        self.type = '_'.join(['Async', self.type])

    async def repos_request(self, org_name, page):
        response = ''
        async with aiohttp.ClientSession(headers={"Authorization": f"token {auth.async_auth()}"}) as session:
            async with session.get(f'https://api.github.com/orgs/{org_name}'
                f'/repos?per_page=100&page={page}') as resp:
                status = resp.status
                response = await resp.json()
        return (status, response)

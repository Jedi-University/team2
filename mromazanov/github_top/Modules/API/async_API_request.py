import asyncio
import aiohttp
import oauthlib.oauth1
from . import auth


async def repos_request(org_name, page):
    response = ''
    async with aiohttp.ClientSession(headers={"Authorization": f"token {auth.async_auth()}"}) as session:
        async with session.get(f'https://api.github.com/orgs/{org_name}'
            f'/repos?per_page=100&page={page}') as resp:
            status = resp.status
            response = await resp.json()
    return (status, response)

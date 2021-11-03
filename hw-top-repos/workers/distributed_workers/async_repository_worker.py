import asyncio
from functools import reduce

import aiohttp
from aiohttp import ClientSession
from api import GitHubAPI

from ..repository_worker import RepositoryWorker
from ..utils import mapping_repo
from ..worker import Worker


class AsyncRepositoryWorker(Worker):
    def __init__(self, organizations_with_repository_urls: dict[int, str], api: GitHubAPI):
        self.repository_urls: list = list(organizations_with_repository_urls.values())
        self.api: GitHubAPI = api

        self.repository_data: list[dict] = list()
        self.worker: RepositoryWorker = RepositoryWorker(organizations_with_repository_urls, api)

    def exec(self) -> list[dict]:
        print(f"{self.__class__.__name__} is working")
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.save_data())
        return self.repository_data

    async def save_data(self) -> None:
        async with aiohttp.ClientSession(headers=self.api.headers) as session:
            data = [await get_repository(session, url) for url in self.repository_urls]
            self.repository_data = reduce(lambda a, b: a + b, data)


async def get_repository(session: ClientSession, url: str) -> list[dict]:
    repository_data: list[dict] = list()
    params = {"page": 1}
    while True:
        async with session.get(url, params=params) as response:
            assert response.status == 200
            data = await response.json()
            if not data:
                break

            params["page"] += 1
            repository_data.extend(map(mapping_repo, data))

    return repository_data

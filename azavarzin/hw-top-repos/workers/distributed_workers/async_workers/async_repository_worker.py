from functools import reduce

from api import GitHubAPI

from .async_worker import AsyncWorker
from workers.repository_worker import RepositoryWorker
from workers.utils import mapping_repo


class AsyncRepositoryWorker(AsyncWorker):
    def __init__(self, organizations_with_repository_urls: dict[int, str], api: GitHubAPI):
        super().__init__(api)
        self.repository_urls: list = list(organizations_with_repository_urls.values())
        self.api: GitHubAPI = api

        self.repository_data: list[dict] = list()
        self.worker: RepositoryWorker = RepositoryWorker(organizations_with_repository_urls, api)

    async def get_data(self):
        data = [await self.get_repository(url) for url in self.repository_urls]
        return reduce(lambda a, b: a + b, data)

    async def get_repository(self, url: str) -> list[dict]:
        params = {"page": 1}
        repository_data: list[dict] = list()
        response = await self.api.get(url)
        while response:
            params["page"] += 1
            repository_data.extend(map(mapping_repo, response))
            response = await self.api.get(url, params=params)

        return repository_data

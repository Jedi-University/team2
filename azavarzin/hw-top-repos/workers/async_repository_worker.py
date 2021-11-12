from functools import reduce

from .async_worker import AsyncWorker
from .utils import mapping_repo


class AsyncRepositoryWorker(AsyncWorker):
    async def get_data(self, repository_urls: list[str]) -> list[dict]:
        data = [await self.get_repository(url) for url in repository_urls]
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

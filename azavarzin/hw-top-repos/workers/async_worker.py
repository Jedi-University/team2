import asyncio
from abc import ABC, abstractmethod

from api import GitHubAPI

from .worker import Worker


class AsyncWorker(Worker, ABC):
    def __init__(self, api: GitHubAPI):
        self.api: GitHubAPI = api

    def exec(self, *args, **kwargs) -> dict[int, str]:
        loop = asyncio.get_event_loop()
        data = loop.run_until_complete(self.get_data(*args, **kwargs))
        return data

    @abstractmethod
    async def get_data(self, *args, **kwargs):
        pass

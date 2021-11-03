from concurrent.futures import ThreadPoolExecutor
from functools import reduce
from multiprocessing import cpu_count

from api.api import GitHubAPI

from ..repository_worker import RepositoryWorker
from ..worker import Worker


class ThreadRepositoryWorker(Worker):
    def __init__(self, organizations_with_repository_urls: dict[int, str], api: GitHubAPI):
        self.repository_urls: list = list(organizations_with_repository_urls.values())

        self.worker: RepositoryWorker = RepositoryWorker(organizations_with_repository_urls, api)

    def exec(self) -> list[dict]:
        print(f"{self.__class__.__name__} is working")
        with ThreadPoolExecutor(max_workers=cpu_count() * 2) as executor:
            result = executor.map(self.worker.get_repository, self.repository_urls)

        return reduce(lambda a, b: a + b, list(result))

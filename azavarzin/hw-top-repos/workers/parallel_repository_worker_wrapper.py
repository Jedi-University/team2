from abc import ABC
from functools import reduce
from multiprocessing import cpu_count

from .repository_worker_wrapper import RepositoryWorkerWrapper
from .worker import Worker


class ParallelRepositoryWorkerWrapper(RepositoryWorkerWrapper, ABC):
    def __init__(self, worker_repository: Worker):
        super().__init__(worker_repository)
        self.pool_executor = None

    def exec(self, repository_urls: list[str]) -> list[dict]:
        super().exec()
        with self.pool_executor(max_workers=cpu_count() * 2) as executor:
            result = executor.map(self.worker_repository.exec, repository_urls)

        return reduce(lambda a, b: a + b, list(result))

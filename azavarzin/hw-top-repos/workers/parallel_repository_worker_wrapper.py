from abc import ABC
from functools import reduce
from multiprocessing import cpu_count

from .worker_wrapper import WorkerWrapper
from .worker import Worker


class ParallelRepositoryWorkerWrapper(WorkerWrapper, ABC):
    def __init__(self, worker: Worker):
        super().__init__(worker)
        self.pool_executor = None

    def exec(self, repository_urls: list[str]) -> list[dict]:
        with self.pool_executor(max_workers=cpu_count() * 2) as executor:
            result = executor.map(self.worker.exec, repository_urls)

        return reduce(lambda a, b: a + b, list(result))

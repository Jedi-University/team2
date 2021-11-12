from concurrent.futures import ThreadPoolExecutor

from .parallel_repository_worker_wrapper import ParallelRepositoryWorkerWrapper
from .worker import Worker


class ThreadRepositoryWorkerWrapper(ParallelRepositoryWorkerWrapper):
    def __init__(self, worker_repository: Worker):
        super().__init__(worker_repository)
        self.pool_executor = ThreadPoolExecutor

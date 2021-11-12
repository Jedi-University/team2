from concurrent.futures import ProcessPoolExecutor

from .parallel_repository_worker_wrapper import ParallelRepositoryWorkerWrapper
from .worker import Worker


class ProcessRepositoryWorkerWrapper(ParallelRepositoryWorkerWrapper):
    def __init__(self, worker_repository: Worker):
        super().__init__(worker_repository)
        self.pool_executor = ProcessPoolExecutor

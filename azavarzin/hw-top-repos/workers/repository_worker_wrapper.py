from .worker import Worker


class RepositoryWorkerWrapper(Worker):
    def __init__(self, worker_repository: Worker):
        self.worker_repository = worker_repository

    def exec(self, *args, **kwargs):
        super().exec(*args, **kwargs)


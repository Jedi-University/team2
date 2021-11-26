from .worker_wrapper import WorkerWrapper


class DefaultRepositoryWorkerWrapper(WorkerWrapper):
    def exec(self, repository_urls: list[str]) -> list[dict]:
        repository_data = []
        for i, url in enumerate(repository_urls, start=1):
            repository_data.extend(self.worker.exec(url))

        return repository_data

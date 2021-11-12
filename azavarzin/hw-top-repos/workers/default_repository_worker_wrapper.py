from .repository_worker_wrapper import RepositoryWorkerWrapper


class DefaultRepositoryWorkerWrapper(RepositoryWorkerWrapper):
    def exec(self, repository_urls: list[str]) -> list[dict]:
        super().exec()
        repository_data = []
        for i, url in enumerate(repository_urls, start=1):
            repository_data.extend(self.worker_repository.exec(url))

        return repository_data

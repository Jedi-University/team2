from api.api import GitHubAPI

from .progress_bar import ConsoleProgressBar
from .utils import mapping_repo
from .worker import Worker


class RepositoryWorker(Worker):
    def __init__(self, organizations_with_repository_urls: dict[int, str], api: GitHubAPI):
        self.repository_urls: list = list(organizations_with_repository_urls.values())
        self.api: GitHubAPI = api

        self.repository_data: list[dict] = list()
        self.progress_bar = ConsoleProgressBar(f"{self.__class__.__name__} is working")

    def exec(self) -> list[dict]:
        for i, url in enumerate(self.repository_urls):
            self.repository_data.extend(self.get_repository(url))
            self.progress_bar.update_progress(i + 1, len(self.repository_urls))

        return self.repository_data

    def get_repository(self, url: str) -> list[dict]:
        params = {"page": 1}
        repository_data: list[dict] = list()
        response = self.api.get(url)
        while response:
            params["page"] += 1
            repository_data.extend(map(mapping_repo, response))
            response = self.api.get(url, params=params)

        return repository_data

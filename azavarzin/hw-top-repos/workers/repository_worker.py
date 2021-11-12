from api import GitHubAPI

from .utils import mapping_repo
from .worker import Worker


class RepositoryWorker(Worker):
    def __init__(self, api: GitHubAPI):
        self.api: GitHubAPI = api

    def exec(self, url: str) -> list[dict]:
        params = {"page": 1}
        repository_data: list[dict] = list()
        response = self.api.get(url)
        while response:
            params["page"] += 1
            repository_data.extend(map(mapping_repo, response))
            response = self.api.get(url, params=params)

        return repository_data

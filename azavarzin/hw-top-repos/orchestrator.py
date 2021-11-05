from configparser import ConfigParser

from api import (
    GitHubAPI,
    DefaultGitHubAPI,
    AsyncGitHubAPI
)
from workers import (
    Worker,
    OrganizationWorker,
    RepositoryWorker,
    DatabaseWorker,
    ThreadRepositoryWorker,
    ProcessRepositoryWorker,
    AsyncOrganizationWorker,
    AsyncRepositoryWorker,
)


class Orchestrator:
    def __init__(self, config: ConfigParser):
        self.config: ConfigParser = config

    def run(self) -> None:
        mode = self.config["Build"]["mode"]
        api = get_api(mode, self.config)

        # получаем n организаций
        number_of_organization = int(self.config["GitHub"]["number_of_organization"])
        organization_worker = get_organization_worker(mode, number_of_organization, api)
        data = organization_worker.exec()

        # для кадой организации получаем репозитории
        repository_worker = get_repository_worker(mode, data, api)
        data = repository_worker.exec()

        # отбираем из всех репозиториев топ по количеству звезд
        top_number = int(self.config["GitHub"]["top_number"])
        data = get_top(data, top_number)

        # записываем данные в базу
        database_worker = DatabaseWorker(data)
        database_worker.exec()


def get_api(mode: str, config: ConfigParser) -> GitHubAPI:
    default_api = DefaultGitHubAPI
    apis = {
        "async": AsyncGitHubAPI
    }

    return apis.get(mode, default_api)(config)


def get_organization_worker(mode: str, number_of_organization, api: GitHubAPI) -> Worker:
    default_worker = OrganizationWorker
    workers = {
        "async": AsyncOrganizationWorker
    }

    return workers.get(mode, default_worker)(number_of_organization, api)


def get_repository_worker(mode: str, data: dict[int, str], api) -> Worker:
    default = RepositoryWorker
    workers = {
        "thread": ThreadRepositoryWorker,
        "process": ProcessRepositoryWorker,
        "async": AsyncRepositoryWorker
    }

    return workers.get(mode, default)(data, api)


def get_top(repos_data: list[dict], count: int) -> list[dict]:
    return sorted(repos_data, key=lambda repo: repo["stars_count"], reverse=True)[:count]

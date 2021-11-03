from configparser import ConfigParser

from api import DefaultGitHubAPI, GitHubAPI
from workers import AsyncRepositoryWorker, ThreadRepositoryWorker, ProcessRepositoryWorker
from workers import DatabaseWorker
from workers import OrganizationWorker
from workers import RepositoryWorker


class Orchestrator:
    def __init__(self, config: ConfigParser):
        self.config: ConfigParser = config
        self.api: GitHubAPI = DefaultGitHubAPI(config)

    def run(self):
        # получаем n организаций
        number_of_organization = int(self.config["GitHub"]["number_of_organization"])
        organization_worker = OrganizationWorker(number_of_organization, self.api)
        data = organization_worker.exec()

        # для кадой организации получаем репозитории
        repository_worker = self.get_repository_worker(data)
        data = repository_worker.exec()

        # отбираем из всех репозиториев топ по количеству звезд
        top_number = int(self.config["GitHub"]["top_number"])
        data = get_top(data, top_number)

        # записываем данные в базу
        database_worker = DatabaseWorker(data)
        database_worker.exec()

    def get_repository_worker(self, data: dict[int, str]):
        mode = {
            "default": RepositoryWorker,
            "thread": ThreadRepositoryWorker,
            "process": ProcessRepositoryWorker,
            "async": AsyncRepositoryWorker
        }

        return mode[self.config["Build"]["mode"]](data, self.api)


def get_top(repos_data: list[dict], count: int):
    return tuple(sorted(repos_data, key=lambda repo: repo["stars_count"], reverse=True))[:count]
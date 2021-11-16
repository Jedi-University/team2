from api import AsyncGitHubAPI
from api import DefaultGitHubAPI
from workers import AsyncRepositoryWorker
from workers import DatabaseWorker
from workers import DefaultRepositoryWorkerWrapper
from workers import OrganizationWorker
from workers import ProcessRepositoryWorkerWrapper
from workers import RepositoryWorker
from workers import ThreadRepositoryWorkerWrapper
from workers import TopFilterWorker
from workers import Worker


def get_workers(config) -> list[Worker]:
    mode = config["Build"]["mode"]
    number_of_organization = int(config["GitHub"]["number_of_organization"])
    top_number = int(config["GitHub"]["top_number"])

    apis = {
        "default": DefaultGitHubAPI,
        "async": AsyncGitHubAPI
    }

    api = apis.get(mode, apis["default"])(config)
    repos_worker = RepositoryWorker(api)
    org_worker = OrganizationWorker(number_of_organization, apis["default"])
    filter_worker = TopFilterWorker(top_number)
    db_worker = DatabaseWorker()

    setting_up_workers: dict[str, Worker] = {
        "default": DefaultRepositoryWorkerWrapper(repos_worker),
        "thread": ThreadRepositoryWorkerWrapper(repos_worker),
        "process": ProcessRepositoryWorkerWrapper(repos_worker),
        "async": AsyncRepositoryWorker(api)
    }

    workers = [org_worker, setting_up_workers[mode], filter_worker, db_worker]

    return workers

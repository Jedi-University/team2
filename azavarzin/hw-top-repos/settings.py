from api import AsyncGitHubAPI
from api import DefaultGitHubAPI
from workers import AsyncOrganizationWorker
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
    org_worker = OrganizationWorker(number_of_organization, api)

    setting_up_workers: dict[str, list] = {
        "default": [
            org_worker,
            DefaultRepositoryWorkerWrapper(repos_worker)
        ],
        "thread": [
            org_worker,
            ThreadRepositoryWorkerWrapper(repos_worker)
        ],
        "process": [
            org_worker,
            ProcessRepositoryWorkerWrapper(repos_worker)
        ],
        "async": [
            AsyncOrganizationWorker(number_of_organization, api),
            AsyncRepositoryWorker(api)
        ]
    }

    workers = setting_up_workers[mode]
    workers.extend([TopFilterWorker(top_number), DatabaseWorker()])

    return workers

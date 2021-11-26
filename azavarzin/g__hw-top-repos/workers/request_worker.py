from api import GitHubAPI

from .worker import Worker


class RequestWorker(Worker):
    def __init__(self, api: GitHubAPI):
        self.api = api
